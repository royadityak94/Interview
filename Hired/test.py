from collections import deque
import math

def f(num, sep=''):
    p = []
    while num:
        num, mod = divmod(num, 1000)
        p += f'{mod:03}', 
    return


def main():
    global a, b
    a, b = 0, []
    func(a, b)
    print (a, b)
    pass


main()
