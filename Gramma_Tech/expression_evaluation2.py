import unittest

def evaluate_expressions(expr):
    if not expr:
        return 0
    num = 0
    sign = '+'
    queue = []
    expr += sign
    for i in range(len(expr)):
        # Time Complexity: O(N), Space Complexity: O(N)
        if expr[i].isdigit():
            num = (num * 10) + int(expr[i])
        else:
            if sign in ['+', '-']:
                queue.append(num * int(sign+'1'))
            elif sign == '*':
                queue.append(queue.pop() * num)
            elif sign == '/':
                queue.append(queue.pop() // num)
            sign = expr[i]
            num = 0
    return sum(queue)

def evaluate_expressions_alternate(expr):
    if not expr:
        return 0
    num = 0
    sign = '+'
    expr += sign
    result = 0
    last_expr = 0
    for i in range(len(expr)):
        # Time Complexity: O(N), Space Complexity: O(1)
        if expr[i].isdigit():
            num = (num * 10) + int(expr[i])
        else:
            if sign in ['+', '-']:
                result += num * int(sign+'1')
            elif sign == '*':
                result -= last_expr
                result += last_expr * num
            elif sign == '/':
                result -= last_expr
                result += last_expr // num

            last_expr = num if not sign in ['+', '-'] else num * int(sign+'1')
            sign = expr[i]
            num = 0
    return result

class Test(unittest.TestCase):
    def setUp(self):
        pass
    def test_1(self):
        expr = '121+321/321-231*324+23+34*34'
        self.assertEqual(eval(expr), evaluate_expressions_alternate(expr))
    def test_2(self):
        expr = '121+321/321-231*324+23+34*34'
        self.assertTrue(eval(expr) == evaluate_expressions_alternate(expr))
    def test_3(self):
        expr = '121+321/321-231*324+23+34*34'
        self.assertFalse(eval(expr) != evaluate_expressions_alternate(expr))
    def test_4(self):
        expr = '1+2-3'
        self.assertEqual(eval(expr), evaluate_expressions_alternate(expr))

    def test_5(self):
        expr = '1+2-3'
        self.assertEqual(eval(expr), evaluate_expressions_alternate(expr))
    def tearDown(self):
        pass

def main():
    unittest.main()

main()
