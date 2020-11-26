# Duplicate number in an immutable array | Floyd cycle detection algo | Leetcode #287
# Finding duplicate number in an immutable array of len(N+1) where the numbers are in range of 1-len(N)

def finding_single_duplicates(arr):
    # O(N) | O(1)
    N = len(arr)
    val = arr[0]
    for idx, ele in enumerate(arr[1:]):
        val ^= (idx+1) ^ ele
    return val

# Multiple duplicates using Floyd cycle detection - iterate across array, mark arr[arr[idx]] as negative.
def finding_multiple_duplicates(arr):
    for idx, ele in enumerate(arr):
        if idx == len(arr)-1:
            return arr[-1]
        val = abs(arr[idx]) - 1
        if arr[val] < 0:
            return abs(arr[arr[val]-1])
        arr[val] *= -1
    return

if __name__ == '__main__':
    # print (finding_single_duplicates([1, 4, 3, 4, 2]))
    print (finding_multiple_duplicates([1, 5, 3, 4, 2, 3]))
    print (finding_multiple_duplicates([1, 5, 3, 5, 2, 4]))
    print (finding_multiple_duplicates([5, 4, 1, 2, 5, 3]))
    print (finding_multiple_duplicates([1, 5, 3, 4, 2, 2]))
