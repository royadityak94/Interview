# Source : https://github.com/mission-peace/interview/blob/master/python/dynamic/longest_increasing_subsequence.py
# Find a subsequence in given array in which the subsequence's elements are in sorted order, lowest to highest, and in which the subsequence is as long as possible.
# Time Complexity: O(N^2), Space Complexity: O(N)

def longest_increasing_subsequence(arr):
    length_arr = len(arr)
    longest = float('-inf')

    for idx in range(length_arr-1):
        longest_so_far = longest_increasing_subsequence_recursive(arr, idx+1, arr[idx])
        longest = max(longest, longest_so_far)
    return longest + 1

def longest_increasing_subsequence_recursive(arr, next, curr_val):
    if next == len(arr):
        return 0

    with_next = 0
    if arr[next] > curr_val:
        with_next = 1 + longest_increasing_subsequence_recursive(arr, next+1, arr[next])
    without_next = longest_increasing_subsequence_recursive(arr, next+1, curr_val)
    return max(with_next, without_next)

if __name__ == '__main__':
    # Using recursion
    print (longest_increasing_subsequence([3, 4, -1, 0, 6, 2, 3]))
    print (longest_increasing_subsequence([2, 5, 1, 8, 3]))
