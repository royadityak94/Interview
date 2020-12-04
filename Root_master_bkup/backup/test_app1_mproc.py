import multiprocessing as mp
import mmap
from collections import Counter, defaultdict
from datetime import datetime
import bisect
import os
import csv
import itertools as IT
from functools import partial
import bisect
import sys

INP_FILE_LOCATION = 'generate_data/trip_data_small.txt' #'input/trip_data.txt'
OP_FILE_LOCATION = 'output/trip_data_s2.txt'

chunk_activity = mp.Manager().dict()
global_drivers = mp.Manager().list()
global_drivers += '',
lock = mp.Lock()

def worker(chunks):
    try:
        for chunk in chunks:
            if not chunk:
                continue

            if chunk[0] == 'Driver':
                continue

            if chunk[0] == 'Trip':
                # if len(chunk) != 5:
                #     print ("Strange: ", chunk)
                driver_name, start_time, end_time, distance = chunk[1:]
                end_time = datetime.strptime(end_time, '%H:%M')
                start_time = datetime.strptime(start_time, '%H:%M')
                time_spent = 0.0
                if end_time < start_time:
                    time_spent = (datetime.strptime('23:59', '%H:%M') - start_time).total_seconds() + \
                     (end_time - datetime.strptime('00:00', '%H:%M')).total_seconds() + 60
                else:
                    time_spent = (end_time - start_time).total_seconds()
                distance = float(distance)
                current_trip_speed = (distance * 3600) / time_spent
                if 5 <= current_trip_speed <= 100:
                    with lock:
                        if driver_name not in chunk_activity:
                            chunk_activity[driver_name] = (0, 0)
                        prev_distance, prev_time = chunk_activity[driver_name]
                        chunk_activity[driver_name] = (prev_distance+distance,
                            prev_time + time_spent)
            else:
                print ("Strange: ", chunk)
    except Exception as ex:
        print ("Error: ", ex, ", Caused by: ", chunk)
        sys.exit(-1)
    return

if __name__ == '__main__':
    if not os.path.exists(INP_FILE_LOCATION):
        raise FileNotFoundError

    cores = mp.cpu_count() - 1
    chunksize = 1

    jobs = []
    q = mp.Queue()
    pool = mp.Pool(cores)
    results = []

    with open(INP_FILE_LOCATION, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=' ')
            for chunk in iter(lambda: list(IT.islice(reader, chunksize*cores)), []):
                chunk = iter(chunk)
                pieces = iter(lambda: list(IT.islice(chunk, chunksize)), [])
                #func = partial(worker)
                pool.imap(worker, pieces),

    # wait for jobs to finish
    # for job_i in jobs:
    #     job_i.get()
    #pool.wait()
    # Merging, closing pool
    pool.close()
    pool.join()
    activities_tuples = []
    print ("Length of Keys: ", len(chunk_activity), len(global_drivers))

    for driver, stats in chunk_activity.items():
        miles_driven, tot_time = stats
        bisect.insort(activities_tuples, (-miles_driven, tot_time, driver))
        del chunk_activity[driver]

    template = '%s: %d miles'
    base_path = '/'.join(OP_FILE_LOCATION.split('/')[:-1])
    if not os.path.exists(base_path):
        os.makedirs(base_path, exist_ok=True)
    with open(OP_FILE_LOCATION, mode='w') as file:
        for tot_distance, tot_time, driver in activities_tuples:
            tot_distance *= -1
            to_write = template % (driver, round(tot_distance))
            if tot_distance:
                mean_speed = round(tot_distance * 3600 /tot_time)
                to_write += ' @ %s mph\n' % mean_speed
                file.write(to_write)
            else:
                file.write(to_write+'\n')
