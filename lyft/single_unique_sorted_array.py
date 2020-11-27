# Ref: https://www.youtube.com/watch?v=nMGL2vlyJk0&t=17s
# [1, 1, 2, 2, 3, 4, 4, 5, 5] -> Answer(3)
# Required Complexity: O(logN) | O(1)
from typing import List
from unittest import TestCase, main

# Time Complexity: O(N), Space Complexity: O(1)
def unique_element_naive(arr: List[int]) -> List[int]:
    result = 0
    for ele in arr:
        result ^= ele
    return result if result else -1

def unique_element(arr: List[int]) -> List[int]:
    low, high = 0, len(arr)-1
    # Boundary Check
    if not high: # Single element array
        return arr[0]
    if arr[0] != arr[1]: # First element is unique
        return arr[0]
    elif arr[-1] != arr[-2]: # Last element is unique
        return arr[-1]

    # Partition the array with low, high based on the index value ->
    # Natural trend, new element starts at even index (0, 2, 4, ...)
    # and ends at an odd index (1, 3, 5, 7). If that's not the case, update high, else low
    while low <= high:
        mid = low + (high-low)//2
        if arr[mid-1] != arr[mid] != arr[mid+1]:
            return arr[mid]
        # Evaluating pair : even_index(i = i+1), odd_index(i=i-1)
        elif ((not mid % 2) and arr[mid] == arr[mid+1]) or ((mid % 2) and arr[mid] == arr[mid-1]):
            low = mid + 1
        else:
            high = mid - 1
    return -1

class Test(TestCase):
    def test_1(self):
        arr = [1, 1, 2, 2, 3, 4, 4, 5, 5]
        self.assertEqual(unique_element_naive(arr), 3)
        self.assertEqual(unique_element(arr), 3)

    def test_2(self):
        arr = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6]
        self.assertEqual(unique_element_naive(arr), 6)
        self.assertEqual(unique_element(arr), 6)

    def test_3(self):
        arr = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]
        self.assertEqual(unique_element_naive(arr), -1)
        self.assertEqual(unique_element(arr), -1)

if __name__ == '__main__':
    main()
