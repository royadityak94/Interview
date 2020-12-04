from unittest import main, TestCase
from unittest.mock import Mock
import random
from synthetic_data_generator import generate_random_names, \
    generate_synthetic_activities
from datetime import datetime, timedelta
from enum import Enum
import os
import shutil

class RunningConstants(Enum):
    TMP_DIR = 'test_temp/'

def count_unique_file_entries(file_path, to_count):
    if not os.path.exists(file_path):
        raise FileNotFoundError
    chunks = 4*(1024**2)
    count = 0
    file = open(file_path)
    file_iterator = file.read
    buffered = file_iterator(chunks)

    while buffered:
        count += buffered.count(to_count)
        buffered = file_iterator(chunks)
    file.close()
    return count

class canGenerateRandomNames(TestCase):
    def test_generate_random_names_right_sized(self):
        for size in random.choices(range(1, 20), k=100):
            try:
                self.assertTrue(len(generate_random_names(size, 2)) == size)
            except AssertionError:
                print ("Size mismatch between generated and actual!")
            except Exception as ex:
                print ("Other Exception: ", ex)

    def test_generate_random_names_right_length(self):
        for length in random.choices(range(1, 20), k=100):
            try:
                self.assertEqual(len(generate_random_names(1, length)[0]), length)
            except AssertionError:
                print ("Length mismatch between generated and actual!")
            except Exception as ex:
                print ("Other Exception: ", ex)

    def test_generate_synthetic_activities(self):
        tmp_dir = RunningConstants.TMP_DIR.value
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        output_file_path = os.path.join(tmp_dir, 'test_file.txt')

        for name_size in random.choices(range(20, 100), k=100):
            try:
                generate_synthetic_activities(output_file_path, name_size, verbose=False)
                length_written = count_unique_file_entries(output_file_path, 'Driver')
                self.assertEqual(name_size, length_written)
            except AssertionError:
                print ("Length mismatch between generated and actual!")
            except Exception as ex:
                print ("Other Exception: ", ex)
        shutil.rmtree(tmp_dir)

if __name__ == '__main__':
    main()
