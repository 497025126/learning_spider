# 结点类
class Node():
    def __init__(self,data):
        self.data = data
        self.left = None
        self.right = None

    def printNode(self,node):
        print(node.data,end=' ')

# 二叉树类
class MyTree():
    def __init__(self):
        # 根节点
        self.root = None

    # 先序遍历
    def preOrder(self,node):
        if not node:
            return
        node.printNode(node)
        self.preOrder(node.left)
        self.preOrder(node.right)

    # 中序遍历
    def inOrder(self,node):
        if not node:
            return
        self.inOrder(node.left)
        node.printNode(node)
        self.inOrder(node.right)

    # 后序遍历
    def postOrder(self,node):
        if not node:
            return
        self.postOrder(node.left)
        self.postOrder(node.right)
        node.printNode(node)

    # 广度优先  核心思想是把每一层结点放入列表中
    def breadthFirst(self,node):
        if not node:
            return
        que=[]
        que.append(node)
        while len(que) != 0:
            tmp = que.pop(0)
            tmp.printNode(tmp)
            if tmp.left:
                que.append(tmp.left)
            if tmp.right:
                que.append(tmp.right)
        return

    # 深度优先遍历  que 当做一个栈使用 pop()末尾
    def depthFirst(self,node):
        if not node:
            return
        que = []
        que.append(node)
        while len(que) != 0:
            tmp = que.pop()
            tmp.printNode(tmp)
            # 先右边
            if tmp.right:
                que.append(tmp.right)
            if tmp.left:
                que.append(tmp.left)

    # 建树
    def bulidTree(self):
        # 先制作结点
        n1 = Node(1)
        n2 = Node(2)
        n3 = Node(3)
        n4 = Node(4)
        n5 = Node(5)
        n6 = Node(6)

        # n1作根节点
        self.root = n1#                    1
        n1.left = n2#                   /    \
        n1.right = n3#                 2      3
        n2.left = n4#                /  \    /  \
        n2.right = n5#              4    5       6
        n3.right = n6#

tree = MyTree()
tree.bulidTree()
tree.preOrder(tree.root)
print()
tree.inOrder(tree.root)
print()
tree.postOrder(tree.root)
print()
tree.breadthFirst(tree.root)
print()
tree.depthFirst(tree.root)
