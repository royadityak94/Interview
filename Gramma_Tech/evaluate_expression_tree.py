
class node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

def evaluateExpressionTree(root):
    if not root:
        return 0

    if not root.left and not root.right:
        # Leaf Node
        return int(root.data)

    left = evaluateExpressionTree(root.left)
    right = evaluateExpressionTree(root.right)

    if root.data == '+':
        return left + right
    elif root.data == '-':
        return left - right
    elif root.data == '*':
        return left * right
    elif root.data == '/':
        if int(root.right.data) == 0:
            return 0
        return left // right


def main():
    root = None
    root = node('-')
    root.left = node('+')
    root.left.left = node('*')
    root.left.left.left = node('4')
    root.left.left.right = node('5')
    root.left.right = node('/')
    root.left.right.left = node('8')
    root.left.right.right = node('3')
    root.right = node('-')
    root.right.left = node('/')
    root.right.left.left = node('12')
    root.right.left.right = node('6')
    root.right.right = node('*')
    root.right.right.left = node('4')
    root.right.right.right = node('6')
    print (evaluateExpressionTree(root))

    root = None
    root = node('+')
    root.left = node('*')
    root.left.left = node('5')
    root.left.right = node('4')
    root.right = node('-')
    root.right.left = node('100')
    root.right.right = node('/')
    root.right.right.left = node('20')
    root.right.right.right = node('2')

    print (evaluateExpressionTree(root))

main()
