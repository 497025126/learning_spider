class Node(object):
    def __init__(self , data):
        self.data = data
        self.next = None

    def printData(self):
        print(self.data)

    def printNext(self):
        print(self.next)

class queueLink(object):
    def __init__(self):
        self.header = None

    def queueIn(self,node):
        if not self.header:
            self.header = node
            return None
        p = self.header
        while p.next:
            p = p.next
        p.next = node

    def queueOut(self):
        if not self.header:
            return None
        p = self.header
        self.header = self.header.next
        return p.data


node1 = Node(1)
node2 = Node(2)
node3 = Node(3)
node4 = Node(4)
node5 = Node(5)

queLink = queueLink()

queLink.queueIn(node1)
queLink.queueIn(node2)
queLink.queueIn(node3)
queLink.queueIn(node4)
queLink.queueIn(node5)

print(queLink.queueOut())
print(queLink.queueOut())
print(queLink.queueOut())
print(queLink.queueOut())
print(queLink.queueOut())
print(queLink.queueOut())
print(queLink.queueOut())
