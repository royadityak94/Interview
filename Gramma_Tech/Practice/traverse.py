
class node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = self.right = None


def inorder_traversal(root):
    if not root:
        return

    stack = []
    current = root

    while stack or current:
        if current:
            stack += current,
            current = current.left
        else:
            node = stack.pop()
            print (node.data, end=' ')
            current = node.right
    print()
    return

def preorder_traversal(root):
    if not root:
        return

    stack = [root]
    while stack:
        node = stack.pop()
        print (node.data, end=' ')
        if node.right:
            stack += node.right,
        if node.left:
            stack += node.left,
    print ()
    return

def postorder_traversal(root):
    if not root:
        return

    stack, stack_reverse = [root], []

    while stack:
        node = stack.pop()
        stack_reverse += node,

        if node.right:
            stack += node.right,
        if node.left:
            stack += node.left,

    while stack_reverse:
        node = stack_reverse.pop()
        print (node.data, end=' ')
    print ()
    return

def main():
    root = None
    root = node('-')
    root.left = node('+')
    root.left.left = node('*')
    root.left.left.left = node('4')
    root.left.left.right = node('5')
    root.left.right = node('/')
    root.left.right.left = node('9')
    root.left.right.right = node('3')
    root.right = node('-')
    root.right.left = node('/')
    root.right.left.left = node('12')
    root.right.left.right = node('6')
    root.right.right = node('*')
    root.right.right.left = node('4')
    root.right.right.right = node('6')
    inorder_traversal(root)
    preorder_traversal(root)
    postorder_traversal(root)

main()
