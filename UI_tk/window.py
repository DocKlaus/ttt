import tkinter as tk

from app.model.tttui import TTTUI

root = tk.Tk()
game = TTTUI(root)
root.mainloop()
