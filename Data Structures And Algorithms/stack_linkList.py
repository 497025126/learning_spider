class Node(object):
    def __init__(self,data):
        self.data = data
        self.next = None

class stackLink(object):
    def __init__(self):
        self.header = None
    def pushStack(self,node):
        if not self.header:
            self.header = node
            return None
        p = self.header
        while p.next:
            p = p.next
        p.next = node

    def popStack(self):
        if not self.header:
            return None
        # 只剩下最后一个结点的情况
        if self.header.next == None:
            data = self.header.data
            self.header = None
            return data

        p = self.header
        # p_pre = self.header
        while p.next :
            p_pre = p
            p = p.next
        p_pre.next = None
        return p.data

node1 = Node(1)
node2 = Node(2)
node3 = Node(3)
node4 = Node(4)
node5 = Node(5)

stackL = stackLink()

stackL.pushStack(node1)
stackL.pushStack(node2)
print(stackL.popStack())

stackL.pushStack(node3)

print(stackL.popStack())
stackL.pushStack(node4)
stackL.pushStack(node5)

print(stackL.popStack())
print(stackL.popStack())
print(stackL.popStack())
