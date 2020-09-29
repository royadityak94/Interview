# Python program to evaluate expressions

def perform_evaluation(num_lists, last_operator, number):
    if last_operator in ['+', '-']:
        num_lists += number * int(last_operator+'1'),
    elif last_operator == '*':
        num_lists += num_lists.pop() * number,
    else:
        if number == 0:
            num_lists.pop()
            num_lists += 0,
        else:
            num_lists += num_lists.pop() // number,
    return num_lists



def evaluate_expressions(str_):
    str_ += '+'
    queue = []
    number = 0
    last_operator = None
    for ch in str_:
        if ch == '(':
            queue += last_operator, ch
            last_operator=None
        elif ch == ')':
            # Pop out all until '('
            queue = perform_evaluation(queue, last_operator, number)
            bracket_sum = 0
            while queue[-1] != '(':
                bracket_sum += queue.pop()
            queue.pop() # Popping out '('
            last_operator = queue.pop()
            queue = perform_evaluation(queue, last_operator, bracket_sum)
            last_operator = None
            number = 0
        elif ch.isdigit():
            number = (number*10) + int(ch)
        else:
            if last_operator:
                queue = perform_evaluation(queue, last_operator, number)
            else:
                queue += number,
            number = 0
            last_operator = ch
    return sum(queue)



def main():
    str_ = '2+3*3'
    print (evaluate_expressions(str_))
    print (eval(str_))

    str_='2+3*2/2-3'
    print (eval(str_))
    print (evaluate_expressions(str_))

    str_ = '2+3*(7-3+2)'
    print (eval(str_))
    print (evaluate_expressions(str_))

    # # More complex expressions
    str_='2+3*3+4/2*(4-1)'
    print (eval(str_))
    print (evaluate_expressions(str_))

main()
