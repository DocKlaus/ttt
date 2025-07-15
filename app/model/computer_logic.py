"""
1. Обозначить объект дерева
2. Куда сходил юзер?
перейти в ветку дерева
3. Какие клетки остались?
4. Какая из них самая выигрышная? (если одинаковые, то любая)
5. Сходить
перейти в ветку дерева
"""

import tkinter as tk
import random

from app.model.node import Node


class ComputerLogic:
    def __init__(self):
        """Обозначаем объект дерева"""
        self.current_node = Node.load()

    def select_current_node(self, position):
        """Получаем узел, в рамках которого будет делаться ход"""
        if position is None:
            return
        for child in self.current_node.children:
            if child.position == position:
                self.current_node = child
                return

    def get_next_position(self):
        """Получаем следующий ход"""
        winnable_child = None
        for child in self.current_node.children:
            value = child.value
            if value is not None:
                if winnable_child is None:
                    winnable_child = child

                elif float(value) > float(winnable_child.value):
                    winnable_child = child
                    print(
                        f"child.position: {child.position}, child.value: {value}, len(child.children): {len(child.children)}"
                    )
        if winnable_child is None:
            winnable_child = random.choice(self.current_node.children)
        self.current_node = winnable_child
        return winnable_child.position


# current_move = 0
# logic = ComputerLogic()
# node = logic.get_current_node(position=current_move)
# print(
#     f"node.position: {node.position}, node.value: {node.value}, len(node.children): {len(node.children)}"
# )
# next_position = logic.get_next_position_move(node=node)
# print(next_position)
