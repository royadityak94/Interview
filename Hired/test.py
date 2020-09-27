from collections import deque
import math

def solution(matrix):
    # Type your solution here

    return matrix


def main():
    #print(solution([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    x = {'foo':'bar'}
    y = {'baz': x}
    print (y['baz']['foo'])

    x  = sum([x*x for x in [1, 2, 3]])
    print (x)

#main()


def f(n):
    if n <= 0:
        return 0
    return n + f(int(n/2))

x = f(4)
print (x)
