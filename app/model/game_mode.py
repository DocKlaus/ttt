import tkinter as tk


class GameModeSelection:
    """Класс для создания окна режимов"""

    def __init__(self):
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
        self.selected_mode = self.mode.get()
        self.root.destroy()
