# Finding the majority element using Moore-Voting algorithm
# Ref: https://www.youtube.com/watch?v=n5QY3x_GNDg&t=28s
# Algorithm Steps: 1) Iterate through array such that we increment/decrement current majority.
# 2) At the end of it, using your candidate element(from step-1), verify that its majority, i.e. count(candidate) >= N/2
from typing import List
from unittest import TestCase, main

def find_majority_element(arr: List[int]) -> List[int]:
    # Finding the majority candidate
    current_majority, count = arr[0], 1
    for ele in arr[1:]:
        if ele != current_majority:
            count -= 1
        else:
            count += 1
        if not count:
            current_majority, count = ele, 1

    # Validating our majority 'find'
    total_found = sum([1 for ele in arr if ele == current_majority])
    return current_majority if total_found > (len(arr)//2) else -1

class Test(TestCase):
    def setup(self):
        pass
    def tearDown(self):
        pass
    def test_1(self):
        item = [2, 3, 3, 2, 3, 2, 3, 3]
        self.assertEqual(find_majority_element(item), 3)
    def test_2(self):
        item = [1, 1, 3, 2, 3, 2, 3, 3]
        self.assertEqual(find_majority_element(item), -1)
    def test_3(self):
        item = [1, 1, 1, 1, 3, 2, 3, 1]
        self.assertEqual(find_majority_element(item), 1)

if __name__ == '__main__':
    main()
