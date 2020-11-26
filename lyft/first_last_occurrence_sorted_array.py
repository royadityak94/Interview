# Ref: https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/ (Facebook)
from typing import List
from unittest import TestCase, main
from bisect import bisect_left, bisect_right

def searchRange_naive(arr: List[int], target: int) -> List[int]:
    base_result = (-1, -1)
    if not arr:
        return base_result
    end = None
    for idx, ele in enumerate(arr):
        if ele == target:
            end = idx
            while arr[end+1] == ele:
                end += 1
            break
    if not end:
        return base_result
    return idx, end

def find_left(arr, l, r, target):
    while l < r:
        mid = l + (r-1)//2
        if arr[mid] < target:
            l = mid + 1
        elif arr[mid-1] < target:
            return mid
        else:
            r = mid - 1
    print ("Returning left: ", l)
    return l

def find_right(arr, l, r, target):
    while l < r:
        mid = l + (r-l)//2
        if arr[mid] > target:
            r = mid - 1
        elif arr[mid+1] > target:
            return mid
        else:
            l = mid + 1

    print ("Returning right: ", r)
    return r

def searchRange_binary(arr: List[int], target:int) -> List[int]:
    low, high = 0, len(arr)-1
    start = -1
    while low <= high:
        mid = low + (high-low)//2
        if arr[mid] == target:
            return (find_left(arr, 0, mid, target), find_right(arr, mid, high, target))
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return (-1, -1)

def searchRange_bisect(arr: List[int], target:int) -> List[int]:
    base_result = (-1, -1)
    if not arr:
        return base_result

    low = bisect_left(arr, target)
    if low not in range(len(arr)):
        return base_result
    high = bisect_right(arr, target)-1
    return (low, high)



class Test(TestCase):
    def test_1(self):
        arr, target = [5,7,7,8,8,8,8,8, 10], 8
        self.assertEqual(searchRange_naive(arr, target), (3, 7))
        self.assertEqual(searchRange_binary(arr, target), (3, 7))
        self.assertEqual(searchRange_bisect(arr, target), (3, 7))

    def test_2(self):
        arr, target = [5,7,7, 10, 12, 14, 16], 14
        self.assertEqual(searchRange_naive(arr, target), (5, 5))
        self.assertEqual(searchRange_binary(arr, target), (5, 5))
        self.assertEqual(searchRange_bisect(arr, target), (5, 5))

    def test_3(self):
        arr, target = [5,7,7, 10, 12, 14, 16], 21
        self.assertEqual(searchRange_naive(arr, target), (-1, -1))
        self.assertEqual(searchRange_binary(arr, target), (-1, -1))
        self.assertEqual(searchRange_bisect(arr, target), (-1, -1))

if __name__ == '__main__':
    main()
