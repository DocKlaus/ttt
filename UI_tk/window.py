import tkinter as tk

from app.model.tttui import TTTUI


if __name__ == "__main__":
    root = tk.Tk()
    game = TTTUI(root)
    root.mainloop()
