import tkinter as tk

from app.model.game_ui import UI
from app.model.game_mode import GameModeSelection


if __name__ == "__main__":

    mode_selection = GameModeSelection()
    root = tk.Tk()
    game = UI(root, mode_selection.selected_mode)
    root.mainloop()
