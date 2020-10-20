
def findSubsequence(arr):
    # Write your code here
    totalRecords = 0
    distinct_set = []
    min_removal_arr = []
    distinct_set_count = 0
    flag=False
    for ele in arr:
        totalRecords += 1
        if ele not in distinct_set:
            distinct_set += ele,
            distinct_set_count += 1
        else:
            if min_removal_arr and min_removal_arr[-1] > ele:
                if flag:
                    break
                min_removal_arr = ele,
                flag = True
            else:
                min_removal_arr += ele,
    if len(min_removal_arr) != (totalRecords-distinct_set_count):
        return [-1]
    return min_removal_arr

if __name__ == '__main__':
    arr = [2, 1, 3, 1, 4, 1, 3]
    print (findSubsequence(arr))
    print (findSubsequence([3, 2, 2, 1, 1]))
