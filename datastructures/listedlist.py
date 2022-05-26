class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def shift(self, node):
        del self.head.next
        self.head.next = None
        node.next = self.head
        self.head = node
