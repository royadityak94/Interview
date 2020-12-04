# -*- coding: utf-8 -*-
# Helper scripts used by  other code files
from collections import Counter
from datetime import datetime
from bisect import insort
import os
from enum import Enum
import pandas as pd
import math

class RunningConstants(Enum):
    """Controllable Hyperparameters
    Supports centralized update of various constant variables used in other pieces of code,
    without the need to update the actual code files.
    """
    TMP_DIR = '../tmp/'
    OUTPUT_DIR = '../output/'
    LOG_DIR = '../log/'
    RESULTSET_TOLERANCE = 10
    MP_CHUNK_SIZE = 512*1024
    MP_CHUNK_PROCESSING_FACTOR = 4
    QUEUE_END_FLAG = 'TERMINATE'
    LOG_FILE = 'root_benchmarking.txt'
    GRAPHING_FILE = '../resources/analyzed_runtime.png'

def fetch_base_path(dir_path: str) -> str:
    """Module to fetch base path of a given path.

    Parameters
    ----------
    dir_path*: string variable representing the actual path variable (absolute/relative)
    (* - Required parameters)

    Returns
    -------
    base path as string
    """
    # Return the file name
    if '/' in dir_path:
        base_url_idx = dir_path.rindex('/')+1
        return dir_path[:base_url_idx]
    return dir_path

def custom_rounding_function(val:float)->int:
    """Rounding function logic to bridge the difference in behavior of pandas
    round() on dataframe and default round() of python
    Parameters
    ----------
    val*: Value to be rounded
    (* - Required parameters)

    Returns
    -------
    rounded value (to the nearest integer)
    """
    # Round x.5 to next nearest integer, i,e (x.5) = ceil(x) to overcome pandas .round()
    ceiling = math.ceil(val)
    if ceiling - val <= .5:
        return ceiling
    return ceiling-1

def generate_output_file_path(dir_path: str, extras:str = '') -> str:
    """Builds an output path from the input path variable for different implementation
    of the solution
    Parameters
    ----------
    dir_path*: Support both relative, absolute references to the input file location.
    extras: Supports appending additional identifiers (as string) to the generated
            output path
    (* - Required parameters)

    Returns
    -------
    output path as string
    """
    base_url_idx = dir_path.rindex('/')+1
    file_format_idx = dir_path.rindex('.')
    return os.path.join(RunningConstants.OUTPUT_DIR.value,
        dir_path[base_url_idx:file_format_idx] +
        '_%s_' % extras + datetime.now().strftime('%m%d%H%M') +
        dir_path[file_format_idx:])

def get_time_spent(start_time: str, end_time: str) -> int:
    """Module to return total time between start, end (in seconds)
    Parameters
    ----------
    start_time*: Start time (Format: %H:%M) as string
    end_time*: End time (Format: %H:%M) as string
    (* - Required parameters)

    Returns
    -------
    time difference (in seconds)
    """
    end_time = datetime.strptime(end_time, '%H:%M')
    start_time = datetime.strptime(start_time, '%H:%M')
    time_spent = 0
    # Supports end_time that overflows to next day
    if end_time < start_time:
        time_spent = (datetime.strptime('23:59', '%H:%M') - start_time).total_seconds() + \
         (end_time - datetime.strptime('00:00', '%H:%M')).total_seconds() + 60
    else:
        time_spent = (end_time - start_time).total_seconds()
    return time_spent

def count_lines_in_file(file_path, to_read='\n'):
    """Module to support light-weight read of a given char in file
    Parameters
    ----------
    file_path*: Support both relative, absolute references to the file to be read.
    to_read: Character identifier that needs to be counted in that file (default: line delimiter)
    (* - Required parameters)

    Returns
    -------
    count of the to_read char in the furnished file
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError

    # Lightest way to read char of interest (in this case, line delimiter) in a given file
    chunks = 4*(1024**2)
    count = 0
    file_ptr = open(file_path)
    file_iterator = file_ptr.read
    buffered = file_iterator(chunks)

    while buffered:
        count += buffered.count(to_read)
        buffered = file_iterator(chunks)
    file_ptr.close()
    return count

def log_appender(information: dict) -> None:
    """Module to support logging of the various python implementations
    Parameters
    ----------
    information*: dictionary furnishing the information about the input_file,
                  output_file, and time_taken
    (* - Required parameters)

    Returns
    -------
    None
    """
    # Extract the necessary information from the dictionary
    time_taken = information['time_taken']
    input_file = information['input_file']
    output_file = information['output_file']
    input_data_volume = count_lines_in_file(input_file)
    output_data_volume = count_lines_in_file(output_file)
    # Build up the output log file path
    log_dir = RunningConstants.LOG_DIR.value
    log_file = os.path.join(log_dir, RunningConstants.LOG_FILE.value)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    template = 'Log Timed %s: Input File: %s, Output File: %s, Input Data Size: %s, ' + \
        'Output Data Size: %s -> Time Taken: %s.\n'
    # Complete appending the log to the existing log file or create new file.
    with open(log_file, mode='a') as file:
        file.write(template % (datetime.now().strftime('%Y%m%d_%H%M'),
            input_file, output_file, input_data_volume, output_data_volume, time_taken))
    return

def write_to_file(file_dir: str, chunk_activity:dict) -> None:
    """Module to write a Counter/shelve/dictionary instance to a file
    Parameters
    ----------
    file_dir*: Support both relative, absolute references to the file to be written to.
    chunk_activity*: the data-structure holding the key-value store
    (* - Required parameters)

    Returns
    -------
    None
    """
    activities_tuples = []
    iterator = None
    flag_counter = False
    if isinstance(chunk_activity, Counter):
        flag_counter = True
        for driver, stats in iter(chunk_activity.most_common()):
            # Time Complexity: O(NLogN), Space Complexity: O(1)
            activities_tuples += (stats + (driver, )),
            del chunk_activity[driver]
    else:
        for driver, stats in chunk_activity.items():
            miles_driven, tot_time = stats
            # Maintains a sorted tuple (in an online fashion) -> Time Complexity: O(NLogN)
            # Space Complexity: O(1)
            insort(activities_tuples, (-miles_driven, tot_time, driver))
            del chunk_activity[driver]

    template = '%s: %d miles'
    base_path = fetch_base_path(file_dir)

    if base_path and not os.path.exists(base_path):
        os.makedirs(base_path, exist_ok=True)

    # Constant space write to file
    with open(file_dir, mode='w') as file:
        for tot_distance, tot_time, driver in activities_tuples:
            if not flag_counter:
                tot_distance *= -1
            to_write = template % (driver, custom_rounding_function(tot_distance))
            if tot_distance:
                mean_speed = round(tot_distance * 3600 /tot_time)
                to_write += ' @ %s mph\n' % mean_speed
                file.write(to_write)
            else:
                file.write(to_write+'\n')
    return
