# Given an array of integers arr, write a function absSort(arr), that sorts the array according to the absolute values of the numbers in arr. If two numbers have the same absolute value, sort them according to sign, where the negative numbers come before the positive number

def simpled_sorted(arr):
    # Simple approach using key parameter in sorted
    return sorted(arr, key=lambda x: (abs(x), x))

def absSort(arr):
    # Using Merge Sort
    if len(arr) == 1:
        return
    mid = len(arr)//2
    left = arr[:mid]
    right = arr[mid:]

    absSort(left)
    absSort(right)

    i = j = k = 0
    while i < len(left) and j < len(right):
        if abs(left[i]) < abs(right[j]) or (abs(left[i]) == abs(right[j]) and left[i] < right[j]) :
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1

    return arr


def main():
    arr = [2, -2, -7, 1, 7, 5, -3, -4, 8]
    print ("Is the merge sort implementation correct: ", simpled_sorted(arr) == absSort(arr))

main()
