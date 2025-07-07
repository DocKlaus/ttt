import tkinter as tk
from app.model.node import Node
from app.model.tttui import TTTUI

# Константы для значений узлов
WIN_VALUE = 1
DRAW_VALUE = 0.5
LOSE_VALUE = 0


def fill_game_tree(root: Node, game: TTTUI) -> None:
    """Рекурсивно заполняет дерево игровых состояний.

    Args:
        root: Корневой узел для заполнения
        game: Объект игры в крестики-нолики
    """
    if not game.game_active:
        return

    # Инициализация дочерних узлов для доступных ходов
    if not root.children:
        for field in game.get_available_fields():
            root.add_child(Node(position=field))

    total_score = 0
    for child in root.children:
        if child.value == 1:
            root.value = 0
            break

        if child.value is not None:
            # Уже рассчитанное значение используем для расчета
            total_score += child.value
            continue

        # Симулируем ход
        game.make_move(child.position, game.current_player)

        # Проверка условий окончания игры
        is_win = game.check_win(False)
        is_draw = game.check_game_over(False)

        if is_win:
            child.value = WIN_VALUE
            return
        elif is_draw:
            child.value = DRAW_VALUE
            return
        else:
            # Рекурсивный вызов для следующего уровня дерева
            fill_game_tree(child, game)
            return

    # Расчет значения для текущего узла
    if root.value is None and root.children:
        root.value = 1 - (total_score / len(root.children))


def start():
    """Основная функция инициализации и выполнения программы"""
    # Инициализация игрового дерева и интерфейса
    root_tree = Node()
    game_window = tk.Tk()
    game = TTTUI(game_window)

    # Максимальное количество итераций для безопасности
    MAX_ITERATIONS = 100000
    iteration = 0

    # Построение дерева решений
    while root_tree.value is None and iteration < MAX_ITERATIONS:
        game.reset_game()
        fill_game_tree(root_tree, game)
        iteration += 1

    print(f"Построение дерева закончено за {iteration} итераций")
    print(root_tree)


start()