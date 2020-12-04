# -*- coding: utf-8 -*-
# Code for implementing task using simple counter
import mmap
from collections import Counter
from utilities import get_time_spent, write_to_file, generate_output_file_path, \
    log_appender
import argparse
import os
import time

def naive_implementation(input_file: str, output_file: str=None) -> str:
    """Naive implementation
    This module implements naively the task of generating the report comprised
    of the total driven miles and the average speed. All numerical data reported
    have been rounded to the nearest integer.

    For usage pattern and motivating examples, refer to the test folder.

    Parameters
    ----------
    input_file*: Support both relative, absolute references to the input file location.
    output_file: Support both relative, absolute references to the output file location.

    (* - Required parameters)

    Returns
    -------
    output file location (for sharing with downstream tasks, if needed).
    """
    # Returning error should the supplied file be missing
    if not os.path.exists(input_file):
        raise FileNotFoundError

    if not output_file:
        output_file = generate_output_file_path(input_file, 'naive')

    activities_map = Counter() # Registering the chunk counter
    task_start_time = time.time()
    with open(input_file, mode='r', encoding='utf-8') as file:
        with mmap.mmap(file.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
            try:
                chunks = mmap_obj.read().decode() + '\n'
                idx = 0
                line = ''
                while idx < len(chunks):
                    if not (chunks[idx] == '\n'):
                        line += chunks[idx]
                    else:
                        if 'Driver' in line:
                            activities_map[line[7:]] = (0, 0)
                        elif 'Trip' in line:
                            driver_name, start_time, end_time, distance = line[5:].split()
                            time_spent = get_time_spent(start_time, end_time)
                            distance = float(distance)
                            current_trip_speed = (distance * 3600) / time_spent
                            if 5 <= current_trip_speed <= 100:
                                if driver_name not in activities_map:
                                    activities_map[driver_name] = (0, 0)
                                # Processing the key-values
                                prev_distance, prev_time = activities_map[driver_name]
                                activities_map[driver_name] = (prev_distance+distance,
                                    prev_time + time_spent)
                        line = ''
                    idx += 1
            except ZeroDivisionError as zde:
                print ('Time-Spent maybe zero: ' + str(time_spent))
                print ("Error: ", ex)
            except KeyError as ke:
                print ('Driver Name may not be in the central dictionary: ')
                print ("Error: ", ex)
            except IOError as ioe:
                print ('I/O Error({0}): {1}'.format(ioe.errno, ioe.strerror))
                print ("Error: ", ex)
            except Exception as ex:
                print ("Error: ", ex)
        task_total_time = time.time() - task_start_time

        # Preparing the final dataset and completing the output file
        write_to_file(output_file, activities_map)
        log_appender({'input_file': input_file, 'output_file': output_file,
            'time_taken': task_total_time})
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
    args = parser.parse_args()
    # Throwing error, should the input argument be missing
    if not args.input:
        parser.error("Missing *required --input argument")

    try:
        # Completing the implementation and returning output file path for
        # application in downstream tasks (necessary when the -o/--output is missing,
        # as the output file name is system generated).
        output_file_path = naive_implementation(args.input, args.output)
        print ("Successfully generated output in file: ", output_file_path)
    except Exception as ex:
        print ("Oh no, something went wrong. Look below for the exception")
        print (ex)
