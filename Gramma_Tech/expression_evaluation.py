
def evaluate_expressions(expr):
    if not expr:
        return 0

    stack = []
    sign = '+'
    expr += '+'
    num = 0

    for i in range(len(expr)):
        if expr[i].isdigit():
            num = (num*10) + int(expr[i])
        else:
            if sign in ['+', '-']:
                stack.append(num * int(sign+'1'))
            elif sign == '*':
                stack.append(stack.pop()*num)
            elif sign == '/':
                stack.append(stack.pop()//num)
            num = 0
            sign = expr[i]
    return sum(stack)

def evaluate_complex_expressions(expr):
    if not expr:
        return 0

    queue = []
    stack = []
    num = 0
    sign = '+'

    for i in range(len(expr)):
        if expr[i].isDigit():
            num = (num*10) + int(expr[i])
        else:
            if sign in ['+', '-']:
                queue.append(num * int(sign+'1'))
            elif sign == '*':
                queue.append(queue.pop()*num)
            elif sign == '/':
                queue.append(queue.pop()//num)

            num = 0
            sign = expr[i]
    return sum(queue)


def main():
    str='2+3*2/5-3'
    print (eval(str))
    print (evaluate_expressions(str))

    # More complex expressions
    str='2+3*(3+4/2*(4-1))'
    print (eval(str))

main()
