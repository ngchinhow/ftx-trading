class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def shift(self, node):
        last_node = self.head.next
        self.head.next = None
        node.next = self.head
        self.head = node
        del last_node
