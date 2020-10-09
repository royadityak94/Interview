import random

class Sorting:
    def __init__(self, arr):
        self.arr = arr

    def bubble_sort(self):
        for i in range(len(self.arr)):
            for j in range(len(self.arr)-i-1):
                if self.arr[j+1] < self.arr[j]:
                    self.arr[j+1], self.arr[j] = self.arr[j], self.arr[j+1]
        return self.arr

    def selection_sort(self):
        for i in range(len(self.arr)):
            index = i
            for j in range(i+1, len(self.arr)):
                if self.arr[j] < self.arr[index]:
                    index = j
            self.arr[i], self.arr[index] = self.arr[index], self.arr[i]
        return self.arr

    def insertion_sort(self):
        for i in range(1, len(self.arr)):
            pivot = self.arr[i]
            j = i-1
            while j >= 0 and pivot < self.arr[j]:
                j -= 1
                self.arr[j+1] = self.arr[j]
            self.arr[j+1] = pivot
        return self.arr

    def merge_sort(self):
        return self.merge_sort_helper(self.arr[:])

    def merge_sort_helper(self, arr):
        if len(arr) == 1:
            return

        mid = len(arr)//2
        left = arr[:mid]
        right = arr[mid:]
        self.merge_sort_helper(left)
        self.merge_sort_helper(right)

        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
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

    def quick_sort(self):
        return self.quick_sort_helper(self.arr[:], 0, len(self.arr)-1)

    def partition(self, arr, low, high):
        i = low-1
        pivot = arr[high]
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i+1], arr[high] = arr[high], arr[i+1]
        return i+1


    def quick_sort_helper(self, arr, low, high):
        if low < high:
            pi = self.partition(arr, low, high)
            self.quick_sort_helper(arr, low, pi-1)
            self.quick_sort_helper(arr, pi+1, high)
        return arr

if __name__ == '__main__':
    arr = list(range(1, 25))
    random.shuffle(arr)
    sorted_arr = arr[:]
    sorted_arr.sort()
    print ("Input Array: ", arr)
    print ("Sorted Array: ", sorted_arr)
    print ("Bubble Sort: ", Sorting(arr).bubble_sort()== sorted_arr)
    print ("Selection Sort: ", Sorting(arr).selection_sort() == sorted_arr)
    print ("Insertion Sort: ", Sorting(arr).insertion_sort() == sorted_arr)
    print ("Merge Sort: ", Sorting(arr).merge_sort() == sorted_arr)
    print ("Quick Sort: ", Sorting(arr).quick_sort() == sorted_arr)
