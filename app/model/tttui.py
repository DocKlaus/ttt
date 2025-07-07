import tkinter as tk
from tkinter import messagebox
import random


class TTTUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-нолики")
        self.current_player = "X"  # X - игрок, O - компьютер
        self.board = [""] * 9
        self.game_active = True

        # История
        self.info_label = tk.Label(root, text="Ваш ход (X)", font=("Arial", 12))
        self.info_label.grid(row=3, column=0, columnspan=3, pady=10)

        # Кнопки поля
        self.buttons = []
        for i in range(9):
            button = tk.Button(
                root,
                text="",
                font=("Arial", 20),
                width=3,
                height=1,
                bg="#f0f0f0",
                command=lambda idx=i: self.player_move(idx),
            )
            button.grid(row=i // 3, column=i % 3, padx=2, pady=2)
            self.buttons.append(button)

        # Кнопка новой игры
        tk.Button(root, text="Новая игра", command=self.reset_game).grid(
            row=4, column=0, columnspan=3
        )

    def reset_game(self):
        self.current_player = "X"
        self.board = [""] * 9
        self.game_active = True
        for button in self.buttons:
            button.config(text="")
        self.info_label.config(text="Ваш ход (X)")

    def player_move(self, idx):
        if not self.game_active or self.board[idx] != "":
            if not self.game_active:
                self.info_label.config("Конец")
            else:
                self.info_label.config(text=f"Клетка {idx + 1} уже занята!")
                return

        self.make_move(idx, "X")
        if not self.check_game_over():
            self.root.after(500, self.computer_move)

    def computer_move(self):
        if not self.game_active:
            return

        # Рандомный ход
        empty_cells = [i for i, cell in enumerate(self.board) if cell == ""]
        if empty_cells:
            move = random.choice(empty_cells)
            self.make_move(move, "O")
            self.check_game_over()

    def make_move(self, idx, player):
        self.board[idx] = player
        self.buttons[idx].config(text=player)
        self.current_player = "O" if player == "X" else "X"
        self.info_label.config(
            text=f"Ход: {'Ваш (X)' if self.current_player == 'X' else 'Компьютер (O)'}"
        )

    def check_game_over(self):
        # Проверка победы
        win_combinations = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
        ]

        for combo in win_combinations:
            a, b, c = combo
            if self.board[a] == self.board[b] == self.board[c] != "":
                winner = "Вы" if self.board[a] == "X" else "Компьютер"
                messagebox.showinfo("Игра окончена", f"{winner} победили!")
                self.game_active = False
                return True

        # Ничья
        if "" not in self.board:
            messagebox.showinfo("Игра окончена", "Ничья!")
            self.game_active = False
            return True

        return False
