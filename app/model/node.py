class Node:
    def __init__(self, position = None, value = None):
        self.position = position
        self.value = value
        self.children = []

    def __str__(self):
        return f"position: {self.position}, value: {self.value}, children: [{len(self.children)}]"

    def add_child(self, child_node):
        self.children.append(child_node)