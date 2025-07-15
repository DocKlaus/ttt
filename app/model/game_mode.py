import tkinter as tk


class GameModeSelection:
    """Создание окна, где выбирается режим игры:
    1. Игрок против Игрока
    2. Игрок против Компьютера
    3. Компьютер против Компьютера
    """

    def __init__(self):
        """Инициализация:
        1. Объект - root
        2. Заголовок окна - root.title
        3. Флаг выбора режима - selected_mode = None
        4. Лейбл с текстом
        5. Список вариантов режима
        6. Создание объектов-кнопок для выбора режима
        7. Кнопка начать игру
        """
        self.root = tk.Tk()
        self.root.title("Выбор режима игры")
        self.selected_mode = None

        tk.Label(self.root, text="Выберите режим игры:", font=("Arial", 14)).pack(
            pady=10
        )

        modes = [
            ("Игрок против Игрока", "PvP"),
            ("Игрок против Компьютера", "PvC"),
            ("Компьютер против Компьютера", "CvC"),
        ]

        self.mode = tk.StringVar(value="PvP")

        for text, mode in modes:
            tk.Radiobutton(
                self.root, text=text, variable=self.mode, value=mode, font=("Arial", 12)
            ).pack(anchor=tk.W, padx=20, pady=20)

        tk.Button(
            self.root,
            text="Начать игру",
            command=self.start_game,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="#000000",
        ).pack(pady=20)

        self.root.mainloop()

    def start_game(self):
        """
        Получаем выбранное значение.
        Закрываем окно выбора режима.
        """
        self.selected_mode = self.mode.get()
        self.root.destroy()
