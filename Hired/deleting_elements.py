# Python deleting elements in O(1) time
import random
from heapq import _siftup, _siftdown


def main():
    ll = [x+1 for x in range(15)]
    print ("Before: ", ll)

    del_idxs = [3, 4, 5, 6]

    for del_idx in del_idxs:
        print ("Deleting: ", del_idx)
        ll[del_idx] = ll[-1]
        del ll[-1]
        if del_idx < len(ll):
            _siftup(ll, del_idx)
            _siftdown(ll, 0, del_idx)
        print (">> ", ll)

    print ("After: ", ll)

main()
