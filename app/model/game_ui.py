import tkinter as tk
from tkinter import messagebox
import random


class UI:
    def __init__(self, root, game_mode="CvC", on_mode_change=None):
        """Инициализация иры и поля"""
        self.root = root
        self.root.title("Крестики-нолики")

        # Настройка главного экрана
        self.root.geometry("400x500")
        self.root.minsize(400, 500)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Центрирование содержимого
        main_frame = tk.Frame(root)
        main_frame.grid(row=1, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Текущий игрок и режим игры
        self.current_player = "X"
        self.board = [""] * 9
        self.game_active = True
        self.waiting_for_computer = False
        self.game_mode = game_mode
        self.on_mode_change = on_mode_change
        self.computer_speed = 1000  # Задержка между ходами компьютера в мс

        # Информационная панель
        self.info_label = tk.Label(
            main_frame,
            text=self.get_status_text(),
            font=("Arial", 16),  # Увеличенный шрифт
        )
        self.info_label.grid(row=0, column=0, pady=(20, 10), sticky="n")

        # Фрейм для игрового поля
        board_frame = tk.Frame(main_frame)
        board_frame.grid(row=1, column=0, sticky="nsew")

        # Настройка пропорций игрового поля
        for i in range(3):
            board_frame.grid_rowconfigure(i, weight=1)
            board_frame.grid_columnconfigure(i, weight=1)

            # Кнопки игрового поля с увеличенным размером
            self.buttons = []
            for i in range(9):
                button = tk.Button(
                    board_frame,
                    text="",
                    font=("Arial", 32),  # Увеличенный шрифт
                    width=3,
                    height=1,
                    bg="#f0f0f0",
                    command=lambda idx=i: self.player_move(idx),
                )
                button.grid(
                    row=i // 3,
                    column=i % 3,
                    padx=5,
                    pady=5,
                    sticky="nsew",  # Растягиваем кнопки
                )
                self.buttons.append(button)

            # Панель управления
            control_frame = tk.Frame(main_frame)
            control_frame.grid(row=2, column=0, pady=(20, 10), sticky="s")

            # Увеличенные кнопки управления
            tk.Button(
                control_frame,
                text="Новая игра",
                command=self.reset_game,
                font=("Arial", 12),
                padx=20,
                pady=10,
            ).pack(side=tk.LEFT, padx=10)

            tk.Button(
                control_frame,
                text="Сменить режим",
                command=self.change_mode,
                font=("Arial", 12),
                padx=20,
                pady=10,
            ).pack(side=tk.LEFT, padx=10)

            # Центрирование окна
            self.center_window()

            if self.game_mode == "CvC":
                self.start_computer_vs_computer()

    def center_window(self):
        """Центрирует окно на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def get_status_text(self):
        if self.game_mode == "PvP":
            return f"Ход игрока {self.current_player}"
        elif self.game_mode == "PvC":
            return (
                f'Ход: {"Ваш (Х)" if self.current_player == "X" else "Компьютер (О)"}'
            )
        else:
            return "Компьютер против компьютера"

    def change_mode(self):
        """Изменение режима игры"""
        self.root.destroy()
        if self.on_mode_change:
            self.on_mode_change()

    def reset_game(self):
        """Играть заново"""
        self.current_player = "X"
        self.board = [""] * 9
        self.game_active = True
        self.waiting_for_computer = False

        for button in self.buttons:
            button.config(text="")

    def new_game(self):
        self.reset_game()

        self.info_label.config(
            text="",
            state=tk.NORMAL,
        )

        self.info_label.config(text=self.get_status_text())

        if self.game_mode == "CvC":
            self.start_computer_vs_computer()

    def start_computer_vs_computer(self):
        self.game_active = True
        for button in self.buttons:
            button.config(state=tk.DISABLED)
        self.computer_move()

    def player_move(self, idx):
        """Ход игрока"""
        if not self.game_active or self.waiting_for_computer:
            return

        if self.board[idx] != "":
            self.info_label.config(text=f"Клетка {idx + 1} уже занята!")
            return

        if self.game_mode == "PvC" and self.current_player != "X":
            return

        self.make_move(idx, self.current_player)

        if not self.check_game_over():
            if self.game_mode == "PvC" and self.current_player == "O":
                self.waiting_for_computer = True
                for button in self.buttons:
                    button.config(state=tk.DISABLED)
                self.root.after(500, self.computer_move)

    def computer_move(self):
        """Ход компьютера"""
        if not self.game_active:
            return

        # Рандомный ход
        empty_cells = [i for i, cell in enumerate(self.board) if cell == ""]
        if empty_cells:
            move = random.choice(empty_cells)
            self.make_move(move, self.current_player)
            self.check_game_over()

        self.continue_computer_game()

    def continue_computer_game(self):
        if self.game_mode == "CvC" and self.game_active:
            self.root.after(self.computer_speed, self.computer_move)
        else:
            self.waiting_for_computer = False
            if self.game_mode == "PvC":
                for button in self.buttons:
                    button.config(state=tk.NORMAL)

    def get_available_fields(self):
        """Вывод доступных клеток"""
        return [i for i, cell in enumerate(self.board) if cell == ""]

    def make_move(self, idx, player):
        """Осуществление хода"""
        self.board[idx] = player
        self.buttons[idx].config(text=player)
        self.current_player = "O" if player == "X" else "X"
        self.info_label.config(text=self.get_status_text())

    def check_win(self, show_message=False):
        """Проверка победы"""
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
                if show_message:
                    if self.game_mode == "PvP":
                        winner = f"Игрок {self.board[a]}"
                    elif self.game_mode == "PvC":
                        winner = "Ты" if self.board[a] == "X" else "Компьютер"
                    else:
                        winner = f"Компьютер {self.board[a]}"
                    messagebox.showinfo("Игра окончена", f"{winner} победил!")
                self.game_active = False
                return True

        return False

    def check_game_over(self, show_message=False):
        """проверка окончания игры"""
        if self.check_win():
            return True

        if "" not in self.board:
            if show_message:
                messagebox.showinfo("Игра окончена", "Ничья")
            self.game_active = False
            return True

        return False
