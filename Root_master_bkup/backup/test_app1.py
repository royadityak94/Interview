import mmap
from collections import Counter
from datetime import datetime
import bisect
import os

INP_FILE_LOCATION = 'generate_data/trip_data.txt' #'input/trip_data.txt'
OP_FILE_LOCATION = 'output/trip_data_final1.txt'

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

def write_to_file(activities_map):
    activities_tuples = []
    for driver, stats in iter(activities_map.most_common()):
        activities_tuples += ((driver, )+ stats),
        del activities_map[driver]

    template = '%s: %d miles'
    base_path = '/'.join(OP_FILE_LOCATION.split('/')[:-1])
    if not os.path.exists(base_path):
        os.makedirs(base_path, exist_ok=True)
    with open(OP_FILE_LOCATION, mode='w+') as file:
        for driver, tot_distance, tot_time in activities_tuples:
            to_write = template % (driver, round(tot_distance))
            if tot_distance:
                mean_speed = round(tot_distance * 3600 /tot_time)
                to_write += ' @ %s mph\n' % mean_speed
                file.write(to_write)
            else:
                file.write(to_write+'\n')
    return

if __name__ == '__main__':
    if not os.path.exists(INP_FILE_LOCATION):
        raise FileNotFoundError
    activities_map = Counter()

    with open(INP_FILE_LOCATION, mode='r', encoding='utf-8') as file:
        with mmap.mmap(file.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
            try:
                chunks = mmap_obj.read().decode('utf-8') + '\n'
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
                                prev_distance, prev_time = activities_map[driver_name]
                                activities_map[driver_name] = (prev_distance+distance,
                                    prev_time + time_spent)
                        line = ''
                    idx += 1
            except ZeroDivisionError as zde:
                print ('Time-Spent maybe zero: ' + str(time_spent))
            except KeyError as ke:
                print ('Driver Name may not be in the central dictionary: ')
            except IOError as ioe:
                print ('I/O Error({0}): {1}'.format(ioe.errno, ioe.strerror))
            except Exception as ex:
                print ("Error: ", ex)
    write_to_file(activities_map)
