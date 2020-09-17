from segment_tree import SegmentTree

def main():
    # Operation: O(logN)
    arr = [3, 1, 5, 3, 13, 7, 2, 7, 2]
    tree = SegmentTree(arr) # Time: O(N), Space: O(N)
    # Sum
    print ("Sum from 1 to 3", arr[1:4], tree.query(1, 3, 'sum'))
    print ("Sum from 4 to 7", arr[4:8], tree.query(4, 7, 'sum'))

    # Min
    print ("Min from 1 to 3", arr[1:4], tree.query(1, 3, 'min'))
    print ("Min from 4 to 7", arr[4:8], tree.query(4, 7, 'min'))

    # Max
    print ("Max from 1 to 3", arr[1:4], tree.query(1, 3, 'max'))
    print ("Max from 4 to 7", arr[4:8], tree.query(4, 7, 'max'))

main()
