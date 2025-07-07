class TTTUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Field')
        self.current_player = 'X'
        self.board = [''] * 9

        self.buttons = []
        for i in range(9):
            button = tk.Button(
                root,
                text='',
                font=('Arial', 15),
                width=5,
                height=2,
                bg='#f0f0f0',
                relief='ridge',
                command=lambda idx=i: self.on_click(idx)
            )
            button.grid(row=i // 3, column=i % 3, padx=2, pady=2)
            self.buttons.append(button)

    def on_click(self, idx):
        if self.board[idx] != '':
            return

        self.board[idx] = self.current_player
        self.buttons[idx].config(text=self.current_player)

        self.current_player = 'O' if self.current_player == 'X' else 'X'