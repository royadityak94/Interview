
class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = self.right = None

def evaluateExpressionTree2(root):
    # Using Recursion!
    if not root:
        return 0

    if not root.left and not root.right:
        return int(root.data)

    left = evaluateExpressionTree2(root.left)
    right = evaluateExpressionTree2(root.right)

    if root.data in ['+', '-']:
        return left + (right * int(root.data+'1'))
    elif root.data == '*':
        return left * right
    else:
        if int(root.right.data) == 0:
            return 0
        return left // right


def evaluateExpressionTree(root):
    # Iterative - using preorder traversal (traverse.py) file!
    if not root:
        return

    stack = []
    current = root
    evaluations = []
    last_operator = None
    number = 0
    pre_last = 1

    while stack or current:
        if current:
            stack += current,
            current = current.left
        else:
            node = stack.pop()
            ## Extra logic (outside of preorder traversal) ##
            if node.data.isdigit():
                if (not stack and not current):
                    stack += Node('+'),
                number =  int(node.data)
            else:
                if last_operator:
                    if last_operator == '+':
                        evaluations += number,
                    if last_operator == '-':
                        evaluations += -number*pre_last,
                        pre_last = -1
                    if last_operator == '*':
                        evaluations += evaluations.pop() * number,
                    if last_operator == '/':
                        if number == 0:
                            evaluations.pop()
                            evaluations += 0,
                        evaluations += evaluations.pop() // number,
                else:
                    evaluations += number,
                number = 0
                last_operator = node.data
            ## Extra logic (outside of preorder traversal) ##
            current = node.right


    return sum(evaluations)



def main():
    root = Node('-')
    root.left = Node('+')
    root.left.left = Node('*')
    root.left.left.left = Node('4')
    root.left.left.right = Node('5')
    root.left.right = Node('/')
    root.left.right.left = Node('9')
    root.left.right.right = Node('3')
    root.right = Node('-')
    root.right.left = Node('/')
    root.right.left.left = Node('12')
    root.right.left.right = Node('6')
    root.right.right = Node('*')
    root.right.right.left = Node('4')
    root.right.right.right = Node('6')
    print (evaluateExpressionTree(root))

    root = None
    root = Node('+')
    root.left = Node('*')
    root.left.left = Node('5')
    root.left.right = Node('4')
    root.right = Node('-')
    root.right.left = Node('100')
    root.right.right = Node('/')
    root.right.right.left = Node('20')
    root.right.right.right = Node('2')
    print (evaluateExpressionTree(root))

main()
