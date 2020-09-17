# Given a static-sized array of integers arr, move all zeroes in the array to the end of the array. You should preserve the relative order of items in the array.
# input:  arr = [1, 10, 0, 2, 8, 3, 0, 0, 6, 4, 0, 5, 7, 0],
# output: [1, 10, 2, 8, 3, 6, 4, 5, 7, 0, 0, 0, 0, 0]

import unittest

def moveZerosToEnd(arr):
    i = j = 0
    n = len(arr)

    while j < n:
        if arr[j] != 0:
            arr[i] = arr[j]
            i, j = i+1, j+1
        else:
            j += 1

    while i < n:
        arr[i] = 0
        i += 1
    return arr

class Test(unittest.TestCase):
    def setup(self):
        pass
    def test_1(self):
        arr = [1, 10, 0, 2, 8, 3, 0, 0, 6, 4, 0, 5, 7, 0]
        self.assertEqual(moveZerosToEnd(arr), [1, 10, 2, 8, 3, 6, 4, 5, 7, 0, 0, 0, 0, 0])
    def test_2(self):
        arr = [0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 4]
        self.assertTrue(moveZerosToEnd(arr), [1, 2, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    def tearDown(self):
        pass


def main():
    unittest.main()

main()
