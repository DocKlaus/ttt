import tkinter as tk

from app.model.game_ui import UI
from app.model.game_mode import GameModeSelection


def start_game():
    mode_selection = GameModeSelection()
    if mode_selection.selected_mode:  # Проверяем, что режим выбран
        root = tk.Tk()
        game = UI(root, mode_selection.selected_mode, on_mode_change=start_game)
        root.mainloop()


if __name__ == "__main__":
    start_game()
