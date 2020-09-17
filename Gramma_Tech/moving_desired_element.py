# Python program to move all of the given desired element to either the back/front of the array without changing the relative ordering of the existing elements.
# Logic: Maintaining the count of all other elements and keep swapping them

def move_to_front(arr, ele):
    i = j = len(arr) - 1

    while j >= 0:
        if arr[j] != ele:
            arr[i] = arr[j]
            i, j = i-1, j-1
        else:
            j -= 1

    # Current 'i' points to the first occurrence of 'ele' from right
    while i >= 0:
        arr[i] = ele
        i -= 1

    return arr

def move_to_rear(arr, ele):
    i = j = 0
    while j < len(arr):
        if arr[j] != ele:
            arr[i] = arr[j]
            i, j = i+1, j+1
        else:
            j += 1

    while i < len(arr):
        arr[i] = ele
        i += 1
    return arr

def main():
    arr = [12, 34, 2, 0, 1, 0, 0, 0, 0, 2, 0, 1, 0]
    desired_ele = 0
    print (move_to_front(arr, desired_ele))
    print (move_to_rear(arr, desired_ele))

main()
