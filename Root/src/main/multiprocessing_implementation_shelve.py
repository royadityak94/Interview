# -*- coding: utf-8 -*-
# Code for implementing task using multiprocessing, shelve
import multiprocessing as mp
from datetime import datetime
import os
import shelve
import shutil
from utilities import get_time_spent, write_to_file, RunningConstants, \
    generate_output_file_path, log_appender
from multiprocessing.managers import BaseProxy
import argparse
import time

def slave_node(line: str) -> tuple:
    """Module tasked with processing a line

    Parses, wrangles the input according to the business logic

    Parameters
    ----------
    line*: Represents a single unprocessed line from the input file

    (* - Required parameters)

    Returns
    -------
    Tuple:
        driver_name: Unique identifier key used in dynamic key-value store
        distance: Processed distance (in miles) parsed from the input
        time_spent: Processed journey time (in seconds) parsed from the input
    """
    try:
        # Since the file has strong schema consistency (if not, that's valiated in
        # upstream tasks), we can directly proceed to assign the space delimited text to different variables
        driver_name, start_time, end_time, distance = line.split()
        time_spent = get_time_spent(start_time, end_time)
        distance = float(distance)
        current_trip_speed = (distance * 3600) / time_spent
        # Meeting the business rule - considering only average speed between [5, 100] inclusive
        if 5 <= current_trip_speed <= 100:
            return (driver_name, distance, time_spent)
        return ('', 0.0, 0.0)
    except ZeroDivisionError as zde:
        print ('Time-Spent maybe zero: ' + str(time_spent))
        print ("Error: ", ex, "\nCaused by: ", line)
    except KeyError as ke:
        print ('Driver Name may not be in the central dictionary: ')
        print ("Error: ", ex, "\nCaused by: ", line)
    except IOError as ioe:
        print ('I/O Error({0}): {1}'.format(ioe.errno, ioe.strerror))
        print ("Error: ", ex, "\nCaused by: ", line)
    except Exception as ex:
        print ("Error: ", ex, "\nCaused by: ", line)

def master_node(chunk_start:int, block:int, file_path:str, q:BaseProxy) -> None:
    """Module implementing process wrapper for individual task splits

    Performs aggregation on the file-splits it's operating upon.

    Parameters
    ----------
    chunk_start*: Pointer to the line from the file.
    block*: Explicit chunk size (dynamically provided by the user or through RunningConstants enum).
    file_path*: Support both relative, absolute references to the input file location.
    q*: Multiprocessing manager queue to support FIFO based execution of the processed chunks

    (* - Required parameters)

    Returns
    -------
    None
    """
    with open(file_path, 'r') as f:
        f.seek(chunk_start)
        lines = f.read(block).splitlines()
        process_dict = dict()
        for line in lines:
            if line:
                if 'Driver' in line:
                    # this if block may be redundant (if there's no requirement
                    # to validate Business_Rule-1 and Business_Rule-2 : Refer to
                    # section 'Possible Implementation' in Readme.md file)
                    if not line[7:] in process_dict:
                        # Initializing driver post-registration
                        process_dict[line[7:]] = (0, 0)
                elif line[:4] == 'Trip':
                    driver_name, distance, time_spent = slave_node(line[5:])
                    if len(driver_name):
                        # (Business_Rule-1 and Business_Rule-2 : Refer to
                        # section 'Possible Implementation' in Readme.md file))
                        if driver_name not in process_dict:
                            process_dict[driver_name] = (distance, time_spent)
                        else:
                            current_distance, current_time = process_dict[driver_name]
                            # Adding miles, time_spent to the existing record
                            # in the dictionary
                            process_dict[driver_name] = (current_distance+distance, current_time+time_spent)
        q.put(process_dict)
    return

def extract_chunk_info(file_path:str, size) -> None:
    """Module to support master node in distributing file chunks to the individual cores

    Support iterator access pattern for processing of file chunks across cores

    Parameters
    ----------
    file_path*: Support both relative, absolute references to the input file location.
    size*: Explicit chunk size (dynamically provided by the user or through RunningConstants enum).

    (* - Required parameters)

    Returns
    -------
    None
    """
    fileEnd = os.path.getsize(file_path)
    with open(file_path, 'rb') as f:
        chunkEnd = f.tell()
        while True:
            chunk_start = chunkEnd
            f.seek(size, 1)
            f.readline()
            chunkEnd = f.tell()
            # Returning pointer to the block of interest in the file
            yield chunk_start, chunkEnd - chunk_start
            if chunkEnd > fileEnd:
                 break
    return

def multiprocessing_implementation_shelve(input_file: str, output_file: str=None,
        tmp_dir:str = None, chunk_size: int = None) -> str:
    """Implementation using python's multiprocessing library and shelve

    This module is distinguished from the naive implementation in that it
    exploits the available CPU cores to parallely read the file chunks in an
    attempt to speedup the data-wrangling tasks. And, it's distinguished from the
    multiprocessing_implementation.py file in that it uses Python's shelve over
    Counter as persistent, dynamic key-value store. For detailed analysis refer to
    the Readme.md file.

    For usage pattern and motivating examples, refer to the test folder.

    Parameters
    ----------
    input_file*: Support both relative, absolute references to the input file location.
    output_file: Support both relative, absolute references to the output file location.
    chunk_size: Hyperparameter (supporting tradeoff) controling block size read by each core.

    (* - Required parameters)

    Returns
    -------
    output file location (for sharing with downstream tasks, if needed).
    """
    # Returning error should the supplied file be missing
    if not os.path.exists(input_file):
        raise FileNotFoundError

    if not output_file:
        output_file = generate_output_file_path(input_file, 'mproc')

    # Making use of the existing cpu cores
    cores = mp.cpu_count()
    pool = mp.Pool(cores)
    task_splits = []
    task_queues = mp.Manager().Queue()
    dict_file_path = os.path.join(tmp_dir, 'shelve_dict')
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir)
    # Registering the shelve in the working directory
    chunk_activities = shelve.open(dict_file_path)
    task_start_time = time.time()

    # Job Splitter: Processing chunked file-splits
    for chunk_start, chunkSize in extract_chunk_info(input_file, chunk_size):
        task_splits += pool.apply_async(master_node, (chunk_start, chunkSize, input_file, task_queues)),

    # Job Merge: Catching up with the yet-to-finish processes
    while len(task_splits) > 0:
        task_splits.pop(0).get()
    task_queues.put(RunningConstants.QUEUE_END_FLAG.value)

    # Processing the returned key-values across splits
    for split_dict in iter(task_queues.get, RunningConstants.QUEUE_END_FLAG.value):
        if len(split_dict):
            for driver_name, (distance, time_spent) in iter(split_dict.items()):
                if driver_name not in chunk_activities:
                    chunk_activities[driver_name] = (distance, time_spent)
                else:
                    prev_distance, prev_time = chunk_activities[driver_name]
                    chunk_activities[driver_name] = (prev_distance+distance,
                        prev_time + time_spent)
    task_total_time = time.time() - task_start_time
    # Preparing the final dataset and completing the output file
    write_to_file(output_file, chunk_activities)
    log_appender({'input_file': input_file, 'output_file': output_file,
        'time_taken': task_total_time})

    # clean up of pool, shelve, tmp directories
    pool.close()
    chunk_activities.close()
    shutil.rmtree(tmp_dir)
    return output_file

if __name__ == '__main__':
    # Enabling command-line support to run this file directly from the terminal
    # with support for arguments (required, default)
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "-i",
            "--input",
            help="Input File Path (Relative/Absolute)",
            type=str
        )
    parser.add_argument(
            "-o",
            "--output",
            help="Custom Output File Path (Relative/Absolute)",
            type=str,
            default = ''
        )
    parser.add_argument(
            "-t",
            "--tmpdir",
            help="Temporary Working Dir",
            type=str,
            default = RunningConstants.TMP_DIR.value
        )
    parser.add_argument(
            "-c",
            "--chunksize",
            help="Processable chunk size",
            type=int,
            default = RunningConstants.MP_CHUNK_SIZE.value
        )
    args = parser.parse_args()
    # Throwing error, should the input argument be missing
    if not args.input:
        parser.error("Missing *required --input argument")

    output_file_path = multiprocessing_implementation_shelve(args.input,
        args.output, args.tmpdir, args.chunksize)

    try:
        # Completing the implementation and returning output file path for
        # application in downstream tasks (necessary when the -o/--output is missing,
        # as the output file name is system generated).
        output_file_path = multiprocessing_implementation_shelve(args.input,
            args.output, args.tmpdir, args.chunksize)
        print ("Successfully generated output in file: ", output_file_path)
    except Exception as ex:
        print ("Oh no, something went wrong. Look below for the exception")
        print (ex)
