import mmap
from collections import Counter
from utilities import get_time_spent, write_to_file, generate_output_file_path, \
    log_appender, RunningConstants
import argparse
import os
import time
import shelve
import shutil

def naive_implementation_shelve(input_file: str, output_file: str=None) -> str:
    if not os.path.exists(input_file):
        raise FileNotFoundError

    if not output_file:
        output_file = generate_output_file_path(input_file, 'naive_shelve')
    tmp_dir = RunningConstants.TMP_DIR.value
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir)
    dict_file_path = os.path.join(tmp_dir, 'shelve_naive_dict')
    activities_map = shelve.open(dict_file_path, writeback=True)
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

        # clean up of shelve, tmp directories
        activities_map.close()
        shutil.rmtree(tmp_dir)
        return output_file

if __name__ == '__main__':
    for idx in range(1, 2):
        input_file_path = 'input/trip_data_sized%d.txt' % idx
        naive_implementation_shelve(input_file_path, '')
        print ("Completed executing : ", input_file_path)
    # INP_FILE_LOCATION = 'generate_data/new_sample.txt'
    # OP_FILE_LOCATION = 'output/new_sample_naive1.txt'
    # output_file_path = naive_implementation(INP_FILE_LOCATION, OP_FILE_LOCATION)
    # print ("Successfully generated output in file: ", output_file_path)
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #         "-i",
    #         "--input",
    #         help="Input File Path (Relative/Absolute)",
    #         type=str
    #     )
    #
    # parser.add_argument(
    #         "-o",
    #         "--output",
    #         help="Custom Output File Path (Relative/Absolute)",
    #         type=str,
    #         default = ''
    #     )
    # args = parser.parse_args()
    # if not args.input:
    #     parser.error("Missing *required --input argument")
    #
    # try:
    #     output_file_path = naive_implementation(args.input, args.output)
    #     print ("Successfully generated output in file: ", output_file_path)
    # except Exception as ex:
    #     print ("Oh no, something went wrong. Look below for the exception")
    #     print (ex)
