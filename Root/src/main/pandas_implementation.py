# -*- coding: utf-8 -*-
# Code for implementing task using pandas
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import os
from utilities import fetch_base_path, generate_output_file_path, \
    custom_rounding_function, log_appender
import argparse
import time

def write_to_file(df: pd.DataFrame, output_file_path: str) -> None:
    """Module to write pandas dataframe to file
    This module shapes up the data (as required by the business logic) to
    write to the file (line by line).

    For usage pattern and motivating examples, refer to the test folder.

    Time Complexity: O(N)
    Space Complexity: O(1)

    Parameters
    ----------
    df*: Pandas DataFrame holding the aggregated reporting data.
    output_file_path*: Support both relative, absolute references to the output file location.

    (* - Required parameters)

    Returns
    -------
    None
    """
    template = '%s: %d miles'
    base_path = fetch_base_path(output_file_path)
    if not os.path.exists(base_path):
        os.makedirs(base_path, exist_ok=True)
    with open(output_file_path, mode='w') as file:
        for _, row in df.iterrows():
            driver, tot_distance, speed = row['driver_name'], row['distance'], row['speed']
            to_write = template % (driver, round(tot_distance))
            if tot_distance:
                to_write += ' @ %s mph\n' % round(speed)
                file.write(to_write)
            else:
                file.write(to_write+'\n')
    return

def pandas_implementation(input_file_path: str, output_file_path: str=None) -> str:
    """Implementation using open-source, high-performance data wrangling tool
    like Pandas which supports flexible, easy-to-use data structure.

    This module implements the task of generating the report comprised
    of the total driven miles and the average speed using pandas library.
    All numerical data reported have been rounded to the nearest integer.

    Parameters
    ----------
    input_file_path*: Support both relative, absolute references to the input file location.
    output_file_path: Support both relative, absolute references to the output file location.

    (* - Required parameters)

    Returns
    -------
    output file location (for sharing with downstream tasks, if needed).
    """
    # Returning error should the supplied file be missing
    if not os.path.exists(input_file_path):
        raise FileNotFoundError

    if not output_file_path:
        output_file_path = generate_output_file_path(input_file_path, 'pandas')

    task_start_time = time.time()
    input_file = pd.read_csv(input_file_path, delimiter=' ', header=None, \
    names=['activity', 'driver_name', 'start_time', 'end_time', 'distance']) # Loading the file
    activity_df = input_file.query('activity in "Trip"') # Filtering out only the Trip information
    # Creating columns labelled start_time, end_time, time_spent, estimated_speed
    activity_df['start_time'] = pd.to_datetime(activity_df['start_time'], format='%H:%M')
    activity_df['end_time'] = pd.to_datetime(activity_df['end_time'], format='%H:%M')
    activity_df['time_spent'] = (activity_df['end_time'] - activity_df['start_time']).dt.seconds
    activity_df['estimated_speed'] = activity_df['distance']*3600/activity_df['time_spent']
    # Meeting the business rule - considering only average speed between [5, 100] inclusive
    activity_df = activity_df.query('5 <= (distance*3600)/time_spent <= 100')
    # Grouped by mean
    aggregated_data = activity_df.groupby('driver_name').agg({'distance':'sum', 'time_spent': 'sum'}).sort_values(by='distance', ascending=False).reset_index()
    aggregated_data['speed'] = (aggregated_data['distance']*3600/aggregated_data['time_spent']).apply(round)
    aggregated_data['distance'] = (aggregated_data['distance']).apply(custom_rounding_function)

    # Preparing drivers with no trip activities
    all_drivers = input_file[input_file.groupby('driver_name')['driver_name'].transform('count') == 1].driver_name
    other_drivers = pd.DataFrame({'driver_name': all_drivers, 'distance':0.0, 'speed': 0.0})
    reported_metrics = pd.concat([aggregated_data, other_drivers])
    task_total_time = time.time() - task_start_time

    # Preparing the final dataset and completing the output file
    write_to_file(reported_metrics, output_file_path)
    log_appender({'input_file': input_file_path, 'output_file': output_file_path,
        'time_taken': task_total_time})
    return output_file_path

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
        output_file_path = pandas_implementation(args.input, args.output)
        print ("Successfully generated output in file: ", output_file_path)
    except Exception as ex:
        print ("Oh no, something went wrong. Look below for the exception")
        print (ex)
