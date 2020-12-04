import random
import numpy as np
import string
from datetime import datetime, timedelta
import mmap
import parser

def generate_random_names(size:int, length: int) -> list:
    possibilities = string.ascii_letters + string.digits
    output_names = []
    while len(output_names) != size:
        generated_name = ''.join([random.choice(possibilities) for _ in range(length)])
        if generated_name not in output_names:
            output_names += generated_name,
    return output_names

def generate_start_end_time(interval: int) -> (str, str):
    hour = str(random.randint(0, 23)).zfill(2)
    minute = str(random.randint(0, 59)).zfill(2)
    start_time_str = '%s:%s' % (hour, minute)
    end_time = datetime.strptime(start_time_str, '%H:%M') + timedelta(minutes=interval)
    end_time_str = str(end_time.hour).zfill(2)+':'+str(end_time.minute).zfill(2)
    return (start_time_str, end_time_str)

def generate_synthetic_activities_helper(size: int, time_range_max: int, \
        distance_range_max: int) -> list:
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
    driver_list = generate_random_names(name_size, name_length)
    template_activity = 'Trip %s %s %s %s\n'
    global_count = 0
    to_be_written = ''
    with open(output_file_path, mode='w', encoding='utf-8') as file_obj:
        for driver in driver_list:
            entries = random.randint(activity_size_min, activity_size_max)
            to_be_written += "Driver %s\n" % driver
            tossed = random.random()
            if tossed < tossed_factor_min or tossed > tossed_factor_max:
                continue
            for activity in generate_synthetic_activities_helper(entries,
                time_range_max, distance_range_max):
                to_write = template_activity % (driver, activity[0], activity[1], activity[2])
                to_be_written += to_write
            file_obj.write(to_be_written)
            to_be_written = ''
        if len(to_be_written):
            file_obj.write(to_be_written)
    return

if __name__ == '__main__':
    # Simple test
    output_file_path = '../output/sampled_221.txt'
    generate_synthetic_activities(output_file_path)
