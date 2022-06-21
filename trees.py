from modules import TreeNode
from collections import deque
import math


def Preorder(root):
    if not root:
        return root

    print(root.val, end=" ")
    Preorder(root.left)
    Preorder(root.right)


def Inorder(root):
    if not root:
        return

    Inorder(root.left)
    print(root.val, end=" ")
    Inorder(root.right)


def PostOrder(root):
    if not root:
        return

    PostOrder(root.left)
    PostOrder(root.right)
    print(root.val, end=" ")


def Height(root):
    if not root:
        return 0

    res = max(Height(root.left), Height(root.right)) + 1

    return res


def PrintAtK(root, k):
    if not root:
        return

    if k == 0:
        print(root.val, end=" ")

    PrintAtK(root.left, k - 1)
    PrintAtK(root.right, k - 1)


def levelOrderTraversal(root):

    q = deque()
    q.append(root)

    while q:
        size = len(q)
        while size > 0:
            curr = q.popleft()
            print(curr.val, end=" ")
            if curr.left:
                q.append(curr.left)
            if curr.right:
                q.append(curr.right)

            size -= 1
        print()


def sizeOfBinaryTree(root):
    if not root:
        return 0

    left = sizeOfBinaryTree(root.left)
    right = sizeOfBinaryTree(root.right)
    return left + right + 1


def MaxInBinaryTree(root):
    if not root:
        return -math.inf

    return max(max(MaxInBinaryTree(root.left), MaxInBinaryTree(root.right)), root.val)


def LeftView(root):
    def DFS(root, level):
        nonlocal max_level
        if not root:
            return

        if level > max_level:
            print(root.val)
            max_level = level

        DFS(root.left, level + 1)
        DFS(root.right, level + 1)

    max_level = 0
    DFS(root, 1)


def childrenSum(root):

    if not root:
        return True

    if not root.left and not root.right:
        return True

    sum = 0

    if root.left:
        sum += root.left.val

    if root.right:
        sum += root.right.val

    return sum == root.val and childrenSum(root.left) and childrenSum(root.right)


def BalancedTree(root):
    if not root:
        return 0

    left = BalancedTree(root.left)
    right = BalancedTree(root.right)

    if left == -1:
        return -1

    if right == -1:
        return -1

    if abs(left - right) > 1:
        return -1

    return max(left, right) + 1


def MaxWidth(root):
    if not root:
        return 0

    q = deque()
    q.append(root)
    MAX = -math.inf

    while q:
        size = len(q)
        MAX = max(MAX, size)
        while size > 0:
            curr = q.popleft()

            if curr.left:
                q.append(curr.left)

            if curr.right:
                q.append(curr.right)

            size -= 1

    return MAX


def cTree(inorder, preorder):
    """
    Construct a binary tree given the inorder and preorder traversals.
    """

    def helper(left, right):

        nonlocal preorder_index
        if left > right:
            return None

        root_value = preorder[preorder_index]
        preorder_index += 1
        root = TreeNode(root_value)

        root.left = helper(left, inorder_tab[root_value] - 1)
        root.right = helper(inorder_tab[root_value] + 1, right)

        return root

    inorder_tab = {}
    preorder_index = 0
    for index, values in enumerate(inorder):
        inorder_tab[values] = index

    return helper(0, len(preorder) - 1)


if __name__ == "__main__":

    root = TreeNode(10)
    root.left = TreeNode(20)
    root.right = TreeNode(30)
    root.left.left = TreeNode(40)
    root.left.right = TreeNode(50)
    root.right.left = TreeNode(60)
    root.right.right = TreeNode(70)
    root.right.right.left = TreeNode(80)

    # preorder = [3, 9, 20, 15, 7]
    # inorder = [9, 3, 15, 20, 7]

    # Preorder(root)
    # Inorder(root)
    # PostOrder(root)
    # print(f"Height :", Height(root))
    # PrintAtK(root, 2)
    # levelOrderTraversal(root)
    # print(sizeOfBinaryTree(root))
    # print(MaxInBinaryTree(root))
    # LeftView(root)
    # print(childrenSum(root))
    # print(BalancedTree(root))
    # print(MaxWidth(root))
    # root = cTree(inorder, preorder)
