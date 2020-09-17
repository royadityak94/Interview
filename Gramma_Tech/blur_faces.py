# Python program to implement  blurring by replacing each cell value by an average value
# Ref: https://app.codesignal.com/company-challenges/verkada/GCykhwZcTrusPZfeQ
import sys

def create_padding(img):
    if not img:
        return []
    h, w = len(img)+1, len(img[0])+1
    zero_row = [1/9] * w
    for row in range(h-1):
        img[row].insert(0, 1/9)
        img[row].append(1/9)

    img.insert(0, zero_row)
    img.append(zero_row)
    return img

def blur_faces(img):
    padded = img
    h, w = len(padded), len(padded[0])
    final_arr = [[None for _ in range(w)] for _ in range(h)]

    for row in range(h):
        for col in range(w):
            neighbor_vals = 0
            participating_cells = 0
            for sub_row in range(max(0, row-1), min(h, row+2)):
                for sub_col in range(max(0, col-1), min(w, col+2)):
                    if (sub_row, sub_col) == (row, col):
                        continue
                    neighbor_vals += img[sub_row][sub_col]
                    participating_cells += 1
            final_arr[row][col] = neighbor_vals/participating_cells

    return final_arr

def main():
    print ("Blurred Ouptut: ", blur_faces([[3, 0, 2, 5], [1, 2, 3, 4], [2, 3, 2, 3]]))
    print ("Blurred Ouptut: ", blur_faces([[47,2,37,18,6], [10,12,25,24,21]]))
    print ("Blurred Ouptut: ", blur_faces([[1,4], [7,10]]))
    print ("Blurred Ouptut: ", blur_faces([[2,8], [50,5], [4,52], [50,2], [9,4], [10,4], [4,4], [77,5], [22,3]]))

main()
