import tkinter as tk
from tkinter import messagebox
import random

from app.model.computer_logic import ComputerLogic


class SquareButton(tk.Canvas):
    """Кастомный квадратный виджет для игрового поля"""

    def __init__(self, master, text="", command=None, **kwargs):
        """
        Параметры:
            master — родительский виджет.
            text — текст, который будет отображаться внутри кнопки (по умолчанию пустой).
            command — функция, вызываемая при клике (по умолчанию None).
            **kwargs — дополнительные параметры для Canvas (например, width, height, bg).

        """
        super().__init__(master, **kwargs, highlightthickness=0)
        self.command = command
        self.text = text
        # при изменении размера кнопки она автоматически перерисуется
        self.bind("<Configure>", self._draw_square)
        # привязывает левый клик мыши (<Button-1>) к методу _on_click
        self.bind("<Button-1>", self._on_click)

    def _draw_square(self, event=None):
        """Отрисовка кнопки"""
        self.delete("all")
        # сторона квадрата определяется по минимальной при изменении размера окна
        size = min(self.winfo_width(), self.winfo_height())
        # Рисуем квадрат
        self.create_rectangle(0, 0, size, size, fill="#f0f0f0", outline="black")
        # Добавляем текст в центре
        self.create_text(
            size // 2, size // 2, text=self.text, font=("Arial", size // 2)
        )

    def _on_click(self, event):
        """Обработка клика"""
        if self.command:
            self.command()

    def update_text(self, text):
        """Обновляет текст и перерисовывает клетку с новым текстом"""
        self.text = text
        self._draw_square()


class UI:
    def __init__(self, root, game_mode="CvC", on_mode_change=None):
        # Настройка основного окна
        self.root = root
        self.root.title("Крестики-нолики")
        self.root.geometry("400x500")
        self.root.minsize(400, 500)

        # Инициализация параметров игры
        self.current_player = "X"
        self.current_move = None
        self.board = [""] * 9
        self.game_active = True
        self.waiting_for_computer = False
        self.game_mode = game_mode
        self.on_mode_change = on_mode_change
        self.computer_speed = 1000

        # Основной контейнер
        self.container = tk.Frame(root)
        self.container.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Информационная панель
        self.info_label = tk.Label(
            self.container, text=self.get_status_text(), font=("Arial", 16)
        )
        self.info_label.pack(pady=(0, 20))

        # Игровое поле (3х3)
        self.board_frame = tk.Frame(self.container)
        self.board_frame.pack(expand=True)

        # Создание кнопок поля
        self.buttons = []
        for i in range(9):
            button = SquareButton(
                self.board_frame,
                text="",
                command=lambda idx=i: self.player_move(idx),
                width=100,
                height=100,
                bg="#f0f0f0",
            )
            row, col = divmod(i, 3)
            button.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            self.buttons.append(button)

        # Настройка пропорций
        for i in range(3):
            self.board_frame.grid_rowconfigure(i, weight=1, uniform="board_row")
            self.board_frame.grid_columnconfigure(i, weight=1, uniform="board_col")

        # Панель управления
        control_frame = tk.Frame(self.container)
        control_frame.pack(pady=(20, 0))

        # Кнопка новой игры
        tk.Button(
            control_frame,
            text="Новая игра",
            command=self.new_game,
            font=("Arial", 12),
            padx=20,
            pady=5,
        ).pack(side=tk.LEFT, padx=10)

        # Кнопка смены режима
        tk.Button(
            control_frame,
            text="Сменить режим",
            command=self.change_mode,
            font=("Arial", 12),
            padx=20,
            pady=5,
        ).pack(side=tk.LEFT, padx=10)

        # Горячие клавиши для полноэкранного режима (но без кнопки)
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Центрирование при первом открытии
        self.center_window()

        if self.game_mode == "CvC":
            self.logic = ComputerLogic()
            self.start_computer_vs_computer()

        if self.game_mode == "PvC":
            self.logic = ComputerLogic()

    def center_window(self):
        """Центрирует окно на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def toggle_fullscreen(self, event=None):
        """Переключение полноэкранного режима по F11"""
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))
        self._adjust_layout()

    def exit_fullscreen(self, event=None):
        """Выход из полноэкранного режима по Escape"""
        self.root.attributes("-fullscreen", False)
        self._adjust_layout()

    def _adjust_layout(self):
        """Подгонка размера элементов при изменении окна"""
        self.root.update_idletasks()
        for button in self.buttons:
            button._draw_square()

    def get_status_text(self):
        """ВЫвод текста статуса игры"""
        if self.game_mode == "PvP":
            return f"Ход игрока {self.current_player}"
        elif self.game_mode == "PvC":
            return (
                f'Ход: {"Ваш (X)" if self.current_player == "X" else "Компьютер (O)"}'
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
            button.update_text("")
            button.config(state=tk.NORMAL if self.game_mode != "CvC" else tk.DISABLED)

        # self.info_label.update_text("")
        # self.info_label.config(state=tk.NORMAL)

    def new_game(self):
        """Запуск новой игры с предварительной очисткой поля"""
        self.reset_game()

        self.info_label.config(text=self.get_status_text())

        if self.game_mode == "CvC":
            self.logic = ComputerLogic()
            self.start_computer_vs_computer()

        if self.game_mode == "PvC":
            self.logic = ComputerLogic()

    def start_computer_vs_computer(self):
        """Запуск игры комп против компа"""
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
        self.current_move = idx

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

        self.logic.select_current_node(self.current_move)
        position = self.logic.get_next_position()
        self.make_move(position, self.current_player)
        self.check_game_over()
        self.continue_computer_game()

        # # Рандомный ход
        # empty_cells = [i for i, cell in enumerate(self.board) if cell == ""]
        # if empty_cells:
        #     move = random.choice(empty_cells)
        #     self.make_move(move, self.current_player)
        #     self.check_game_over()
        #
        # self.continue_computer_game()

    def continue_computer_game(self):
        """Продолжение игры"""
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
        self.buttons[idx].update_text(player)
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
