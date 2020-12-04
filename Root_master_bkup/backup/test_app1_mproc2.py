import multiprocessing as mp
from collections import Counter, defaultdict
from datetime import datetime
import os
import time
import bisect
import sys
import shelve
import shutil

# Global Variables
INP_FILE_LOCATION = 'generate_data/trip_data_alternate.txt'
OP_FILE_LOCATION = 'output/trip_data_alternate_mproc.txt'
#chunk_activity = mp.Manager().dict()
CHUNK_SIZE = 1024*1024
lock = mp.Lock()


def get_time_spent(start_time, end_time):
    end_time = datetime.strptime(end_time, '%H:%M')
    start_time = datetime.strptime(start_time, '%H:%M')
    time_spent = 0.0
    if end_time < start_time:
        time_spent = (datetime.strptime('23:59', '%H:%M') - start_time).total_seconds() + \
         (end_time - datetime.strptime('00:00', '%H:%M')).total_seconds() + 60
    else:
        time_spent = (end_time - start_time).total_seconds()
    return time_spent

def write_to_file(chunk_activity):
    activities_tuples = []
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
    return

def worker(line):
    try:
        driver_name, start_time, end_time, distance = line.split()
        time_spent = get_time_spent(start_time, end_time)
        distance = float(distance)
        current_trip_speed = (distance * 3600) / time_spent

        if 5 <= current_trip_speed <= 100:
            return driver_name, distance, time_spent
        else:
            return '', 0.0, 0.0
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
        sys.exit(-1)
        print ("Error: ", ex, "\nCaused by: ", line)
    return

def process_wrapper(chunkStart, chunSize, file_path, q):
    with open(file_path, 'r') as f:
        f.seek(chunkStart)
        lines = f.read(chunSize).splitlines()
        process_dict = dict()#defaultdict(lambda: (0, 0))
        for line in lines:
            if line:
                if 'Driver' in line:
                    if not line[7:] in process_dict:
                        process_dict[line[7:]] = (0, 0)
                    # if not line[7:] in chunk_activity:
                    #     chunk_activity[line[7:]] = (0, 0)
                    pass
                elif line[:4] == 'Trip':
                    driver_name, distance, time_spent = worker(line[5:])
                    if len(driver_name):
                        if driver_name not in process_dict:
                            process_dict[driver_name] = (distance, time_spent)
                        else:
                            current_distance, current_time = process_dict[driver_name]
                            process_dict[driver_name] = (current_distance+distance, current_time+time_spent)
        q.put(process_dict)
    return

def chunkfy(file_path, size=CHUNK_SIZE):
    fileEnd = os.path.getsize(file_path)
    with open(file_path, 'rb') as f:
        chunkEnd = f.tell()
        while True:
            chunkStart = chunkEnd
            f.seek(size, 1)
            f.readline()
            chunkEnd = f.tell()
            yield chunkStart, chunkEnd - chunkStart
            if chunkEnd > fileEnd:
                 break
    return

if __name__ == '__main__':
    # Revert with error should the file not exist
    if not os.path.exists(INP_FILE_LOCATION):
        raise FileNotFoundError

    cores = min(8, mp.cpu_count())
    pool = mp.Pool(cores)
    task_splits = []

    # Job Splitter: Processing file-splits
    q = mp.Manager().Queue()
    for chunkStart, chunkSize in chunkfy(INP_FILE_LOCATION):
        task_splits += pool.apply_async(process_wrapper, (chunkStart, chunkSize, INP_FILE_LOCATION, q)),

    # Job Merge: Hault for all the initiated processes to finish
    while len(task_splits) > 0:
        task_splits.pop(0).get()

    chunk_activities = shelve.open('tmp/files')
    q.put('STOP')
    cnt = 0
    for split_dict in iter(q.get, 'STOP'):
        cnt += 1
        if not cnt % 500:
            print ("Progress : ", cnt)
        if len(split_dict):
            for tuple in split_dict.items():
                driver_name, (distance, time_spent) = tuple
                if driver_name not in chunk_activities:
                    chunk_activities[driver_name] = (distance, time_spent)
                else:
                    prev_distance, prev_time = chunk_activities[driver_name]
                    chunk_activities[driver_name] = (prev_distance+distance,
                        prev_time + time_spent)

    # clean up
    pool.close()

    print ("Preparing to write to file ...")
    # Preparing the final dataset and completing the output file
    write_to_file(chunk_activities)

    chunk_activities.close()
    shutil.rmtree('tmp')
