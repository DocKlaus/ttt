class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)