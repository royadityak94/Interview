# -*- coding: utf-8 -*-
# Code for synthetically producing large input files used for validating,
# benchmarking implementations
import random
import string
from datetime import datetime, timedelta
import mmap
import parser

def generate_random_names(size:int, length: int) -> list:
    """Module to generate random names of a given size and length
    Builds up a random key of a given length using alphanumeric chars [a-z, A-Z, 0-9]

    Parameters
    ----------
    size*: Represents count of total generated keys
    length*: Represents the length of the individual keys (we have modeled a constant length key)
    (* - Required parameters)

    Returns
    -------
    list of string where the (list length) == size paramter.
    """
    possibilities = string.ascii_letters + string.digits
    output_names = []
    while len(output_names) != size:
        generated_name = ''.join([random.choice(possibilities) for _ in range(length)])
        if generated_name not in output_names:
            output_names += generated_name,
    return output_names

def generate_start_end_time(interval: int) -> (str, str):
    """Module to generate random start and end times
    Builds up a random key of a given length using alphanumeric chars [a-z, A-Z, 0-9]

    Parameters
    ----------
    interval*: Represents the difference in minutes between start and end time
    (* - Required parameters)

    Returns
    -------
    Tuple:
        0: Represents start time  (24-hour clock)
        1: Represents end time  (24-hour clock)
    """
    hour = str(random.randint(0, 23)).zfill(2)
    minute = str(random.randint(0, 59)).zfill(2)
    start_time_str = '%s:%s' % (hour, minute)
    end_time = datetime.strptime(start_time_str, '%H:%M') + timedelta(minutes=interval)
    end_time_str = str(end_time.hour).zfill(2)+':'+str(end_time.minute).zfill(2)
    return (start_time_str, end_time_str)

def generate_synthetic_activities_helper(size: int, time_range_max: int, \
        distance_range_max: int) -> list:
    """Helper Module to mock driver activities
    Builds up driver activities of the same length as the size paramter

    Parameters
    ----------
    size*: Count of distinct activities to be generated
    time_range_max: Hyperparameter knob to control the max separation in start, end times
    distance_range_max: Hyperparameter knob to control the max travelled distance
    (* - Required parameters)

    Returns
    -------
    list of activities mimicing an users' activity.
    """
    time_range = range(1, time_range_max) #minutes
    time_weights = [1 for _ in range(1, 25)] + [2 for _ in range(1, 55)] + \
        [3 for _ in range(1, 25)] + [1 for _ in range(1, 18)]
    journey_time = random.choices(time_range, time_weights, k=size)
    distance_range = np.arange(4, distance_range_max, 0.1)
    length_of_distance_range = len(distance_range)
    distance_weights = [1 for _ in range(1, length_of_distance_range//2)] + \
        [2 for _ in range(1, length_of_distance_range//4)] + \
        [3 for _ in range(1, length_of_distance_range//5)]
    for _ in range(length_of_distance_range - len(distance_weights)):
        distance_weights += 1,
    distance = random.choices(distance_range, distance_weights, k=size)
    output = []
    for _ in range(size):
        miles_travelled = str(round(distance.pop(), 1))
        start_time, end_time = generate_start_end_time(journey_time.pop())
        output += [start_time, end_time, miles_travelled],
    return output

def generate_synthetic_activities(output_file_path: str, name_size: int= 1,
        name_length: int = 6, activity_size_min:int = 1,
        activity_size_max: int = 10, tossed_factor_min: int = 0.1,
        tossed_factor_max: int = 0.9, time_range_max:int = 120,
        distance_range_max:int = 150, verbose:bool=True) -> None:
    """Module to randomly populate the entire input file with driver information, activities

    Parameters
    ----------
    output_file_path*: Support both relative, absolute references to the output file location.
    name_size: Hyperparameter controlling distinct driver entries to be created (default: 1)
    name_length:Hyperparameter controlling distinct length of the key (driver) (default: 6)
    activity_size_min: Hyperparameter controlling minimum driver activities to be created (default: 1)
    activity_size_max: Hyperparameter controlling maximum driver activities to be created (default: 10)
    tossed_factor_min: Hyperparameter controlling the left-liklihood of a driver to
                       have zero activities (default: .1)
    tossed_factor_max: Hyperparameter controlling the right-liklihood of a driver to
                       have zero activities (default: .9)
    time_range_max: Hyperparameter controlling maximum driving time (in minutes) for a driver (default: 120)
    distance_range_max: Hyperparameter controlling maximum driving distance (in miles) for a driver (default: 150)
    verbose: Switch to limit/expand verbose of the method
    (* - Required parameters)

    Returns
    -------
    None
    """
    driver_list = generate_random_names(name_size, name_length)
    template_activity = 'Trip %s %s %s %s\n'
    global_count = 0
    print ("Driver Length: ", driver_list)

    with open(output_file_path, mode='w', encoding='utf-8') as file_obj:
        for driver in driver_list:
            to_be_written = ''
            entries = random.randint(activity_size_min, activity_size_max)
            log_divisor = max(1, (name_size*entries//10))
            to_be_written += "Driver %s\n" % driver
            tossed = random.random()
            if tossed < tossed_factor_min or tossed > tossed_factor_max:
                continue
            for activity in generate_synthetic_activities_helper(entries,
                time_range_max, distance_range_max):
                to_write = template_activity % (driver, activity[0], activity[1], activity[2])
                to_be_written += to_write
                global_count += 1
                if verbose and global_count % (log_divisor):
                    print ("Completed writing %d entries ..." % global_count)
            file_obj.write(to_be_written)
            to_be_written = ''
        if len(to_be_written):
            file_obj.write(to_be_written)
    return

if __name__ == '__main__':
    # Simple test
    output_file_path = '../output/sampled_221.txt'
    generate_synthetic_activities(output_file_path)
