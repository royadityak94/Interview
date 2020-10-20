# Finding the longest increasing subsequence in an array
# [3, 4, -1, 0, 6, 2, 3] -> [-1, 0, 2, 3]
# [2, 5, 1, 8, 3] -> [2, 5, 8]

def finding_longest_subsequence(arr):
    if not arr:
        return 0
    longest_subsequence = 1
    longest_arr = [arr[0]]
    max_observed = float('-inf')

    for idx in range(1, len(arr)):
        ele = arr[idx]
        while True:
            if longest_arr and longest_arr[-1] > ele:
                longest_arr.pop(-1)
                longest_subsequence -= 1
            else:
                break
        longest_arr += ele,
        longest_subsequence += 1
        max_observed = max(max_observed, longest_subsequence)

    print (longest_arr, longest_subsequence, max_observed)
    return max_observed

if __name__ == '__main__':
    print (finding_longest_subsequence([3, 4, -1, 0, 6, 2, 3]))
    print (finding_longest_subsequence([2, 5, 1, 8, 3]))
