# https://www.geeksforgeeks.org/inorder-successor-in-binary-search-tree/

class TreeNode:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def inorder_traversal_recursive(self, root):
        if not root:
            return
        self.inorder_traversal_recursive(root.left)
        print (root.data, end = ' -> ')
        self.inorder_traversal_recursive(root.right)

    def inorder_successor(self, root, data):
        if not root:
            return

        next = None
        while root:
            if root.data > data:
                next = root
                root = root.left
            else:
                root = root.right
        return next.data

    def inorder_traversal_iterative(self, root):
        if not root:
            return
        stack, current = [root], root
        while stack or current:
            if current:
                stack += current,
                current = current.left
            else:
                popped = stack.pop()
                print (popped.data, end = ' -> ')
                current = popped.right
        return

    def preorder_traversal_iterative(self, root):
        if not root:
            return
        stack = [root]
        while stack:
            popped = stack.pop()
            print (popped.data, end = ' -> ')
            if popped.right:
                stack += popped.right,
            if popped.left:
                stack += popped.left,
        return

    def postorder_traversal_iterative(self, root):
        if not root:
            return
        stack, stack_reverse = [root], []
        while stack:
            popped = stack.pop()
            stack_reverse += popped,
            if popped.left:
                stack += popped.left,
            if popped.right:
                stack += popped.right,

        while stack_reverse:
            print (stack_reverse.pop().data, end = ' -> ')
        return

    def inorder_successor_iterative(self, root, data):
        if not root or not data:
            return
        stack, current = [root], root
        flag = False
        while stack or current:
            if current:
                stack += current,
                current = current.left
            else:
                popped = stack.pop()
                if flag:
                    return popped.data
                elif popped.data == data:
                    flag = True
                current = popped.right
        return

if __name__ == '__main__':
    root = TreeNode(20)
    root.left = TreeNode(8)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(12)
    root.left.right.left = TreeNode(10)
    root.left.right.right = TreeNode(14)

    root.right = TreeNode(22)
    root.inorder_traversal_recursive(root)
    print ()

    # Printing the inorder successor
    print ("Inorder Successor: ", root.inorder_successor(root, 8))
    print ("Inorder Successor: ", root.inorder_successor(root, 10))
    print ("Inorder Successor: ", root.inorder_successor(root, 14))

    # Exploring various traversals
    print ("Inorder Traversal : ")
    root.inorder_traversal_iterative(root)
    print ()

    print ("Preorder Traversal : ")
    root.preorder_traversal_iterative(root)
    print ()

    print ("Postorder Traversal : ")
    root.postorder_traversal_iterative(root)
    print ()

    print ('--------------------------------------')
    # Printing the inorder successor
    print ("Inorder Successor: ", root.inorder_successor_iterative(root, 8))
    print ("Inorder Successor: ", root.inorder_successor_iterative(root, 10))
    print ("Inorder Successor: ", root.inorder_successor_iterative(root, 14))
