# import collections
# from typing import List
#
# # Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None
#
# class Node_handle:
#     def __init__(self):
#         self.curNode = None
#
#     def addbefore(self, data):
#         for i in data:
#             node = ListNode(i)
#             node.next = self.curNode
#             self.curNode = node
#         return self.curNode
#
#     def addafter(self, data):
#         h1 = h2 = ListNode(0)
#         for i in data:
#             node = ListNode(i)
#             h2.next = node
#             h2 = node
#         return h1.next
#
#     def printNode(self, node):
#         while node:
#             print('\nnode: ', node, 'value: ', node.val, ' next: ', node.next)
#             node = node.next
#
# # Definition for singly-linked list.
# # class ListNode:
# #     def __init__(self, x):
# #         self.val = x
# #         self.next = None
#
# class Solution:
#     def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:
#         hasvisit = set()
#         temp = headA
#         while temp:
#             hasvisit.add(temp)
#             temp = temp.next
#         temp = headB
#         while temp:
#             if temp in hasvisit:
#                 return temp
#             temp = temp.next
#         return None
#
#
#
# if __name__ == '__main__':
#     # 8
#     # [4,1,8,4,5]
#     # [5,0,1,8,4,5]
#     # 2
#     # 3
#     handle = Node_handle()
#     nums1 = [1, 2,3, 4]
#     # h1 = handle.addbefore(nums1)
#     h1 = handle.addafter(nums1)
#     nums2 = [5,2,3,4]
#     h2 = handle.addafter(nums2)
#     handle.printNode(h1)
#     handle.printNode(h2)
#     val = 5
#     print(Solution().getIntersectionNode(h1, h2))
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Tree:
    def __init__(self):
        self.root = TreeNode(-1)

    def add(self, data):
        node = TreeNode(data)
        if self.root.val == -1:
            self.root = node
        else:
            mq = []
            mq.append(self.root)
            while mq:
                treeNode = mq.pop(0)
                if not treeNode.left:
                    treeNode.left = node
                    return
                elif not treeNode.right:
                    treeNode.right = node
                    return
                else:
                    mq.append(treeNode.left)
                    mq.append(treeNode.right)

    def bfs(self, root):
        if root == None:
            return
        q = []
        q.append(root)
        while q:
            no = q.pop(0)
            print(no.val)
            if no.left != None:
                q.append(no.left)
            if no.right != None:
                q.append(no.right)


class Solution:
    def isBalanced(self, root: TreeNode) -> bool:
        def height(root):
            if not root:
                return 0
            return max(height(root.left), height(root.right))+1
        if not root:
            return True
        return abs(height(root.left)-height(root.right))<=1 and self.isBalanced(root.left) and self.isBalanced(root.right)


if __name__ == '__main__':
    # datas = [3, 9, 20, None, None, 15, 7]
    datas = [1,2,2,3,3,None,None,4,4]
    tree = Tree()
    for data in datas:
        tree.add(data)
    # print('qianxu')
    # tree.bfs(tree.root)
    print(Solution().isBalanced(tree.root))


