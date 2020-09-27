class Sort:
    def __init__(self, arr):
        self.arr = arr

    def bubble_sort(self):
        arr = self.arr[:]
        for i in range(len(arr)):
            for j in range(len(arr)-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

    def selection_sort(self):
        arr = self.arr[:]
        for i in range(len(arr)):
            index = i
            for j in range(i+1, len(arr)):
                if arr[j] < arr[index]:
                    index = j
            arr[i], arr[index] = arr[index], arr[i]
        return arr

    def insertion_sort(self):
        arr = self.arr[:]
        for i in range(1, len(arr)):
            item = arr[i]
            j = i-1
            while (j >= 0) and item < arr[j]:
                arr[j+1] = arr[j]
                j -= 1
            arr[j+1] = item
        return arr

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
            i, k = i+1, k+1

        while j < len(right):
            arr[k] = right[j]
            j, k = j+1, k+1

        return arr

    def merge_sort(self):
        return self.merge_sort_helper(self.arr[:])


def main():
    arr = [12, 3, 5, 9, 8, 11, 7, 2]
    sorting = Sort(arr)
    print ("Bubble Sort: ", sorting.bubble_sort())
    print ("Selection Sort: ", sorting.selection_sort())
    print ("Insertion Sort: ", sorting.insertion_sort())
    print ("Merge Sort: ", sorting.merge_sort())

main()
