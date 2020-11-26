# Finding out the final asteroid state after collision
from unittest import TestCase, main
from typing import List
from collections import deque
import sys
def can_collide(prev, curr):
    if (curr < 0 and prev > 0):
        return True
    return False

def asteroidCollision(asteroids:List[int]) -> List[int]:
    if len(asteroids) < 2:
        return asteroids
    moveRight = deque()
    moveRight += asteroids[0],

    for asteroid in asteroids[1:]:
        while moveRight and can_collide(moveRight[-1], asteroid):
            peek = moveRight[-1]
            if peek == -asteroid:
                moveRight.pop()
                break
            elif peek < -asteroid:
                moveRight.pop()
                continue
            else:
                break
        else:
            moveRight += asteroid,
    return list(moveRight)

class Test(TestCase):
    def test_example1(self):
        self.assertEqual(asteroidCollision([5, 10, -5]), [5, 10])
    def test_example2(self):
        self.assertEqual(asteroidCollision([8, -8]), [])
    def test_example3(self):
        self.assertEqual(asteroidCollision([10, 2, -5]), [10])
    def test_example4(self):
        self.assertEqual(asteroidCollision([-2, -1, 1, 2]), [-2, -1, 1, 2])
    def test_example5(self):
        self.assertEqual(asteroidCollision([-2, -2, 1, -2]), [-2, -2, -2])
    def test_example6(self):
        self.assertEqual(asteroidCollision([-2, -2, -2, 1]), [-2, -2, -2, 1])

if __name__ == '__main__':
    main()
