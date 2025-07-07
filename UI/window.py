import tkinter as tk
from tkinter import messagebox

def create_board():
    root = tk.Tk()
    root.title('Field')

    for i in range(9):
        button = tk.Button(
            root,
            text='',
            font=('Arial', 15),
            width=5,
            height=2,
            bg='#f0f0f0',
            relief='ridge'
        )
        button.grid(row=i // 3, column=i % 3, padx=2, pady=2)

    root.mainloop()

create_board()