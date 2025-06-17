import tkinter as tk
from tkinter import messagebox
from typing import List, Optional

class TrisGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tris")
        self.window.configure(bg='#f0f0f0')
        
        # Make window resizable
        self.window.resizable(True, True)
        
        # Configure grid weights for responsiveness
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=1)
        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_rowconfigure(3, weight=1)
        self.window.grid_rowconfigure(4, weight=1)
        
        # Game state
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        
        # Create main container with padding
        self.main_container = tk.Frame(self.window, bg='#f0f0f0', padx=20, pady=20)
        self.main_container.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Create title label
        self.title_label = tk.Label(
            self.main_container,
            text="Tris",
            font=('Helvetica', 24, 'bold'),
            bg='#f0f0f0',
            fg='#333333'
        )
        self.title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Create player turn label
        self.turn_label = tk.Label(
            self.main_container,
            text="Turno del giocatore: X",
            font=('Helvetica', 12),
            bg='#f0f0f0',
            fg='#333333'
        )
        self.turn_label.grid(row=1, column=0, pady=(0, 20))
        
        # Create game board container
        self.board_container = tk.Frame(self.window, bg='#f0f0f0')
        self.board_container.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=20, pady=10)
        
        # Configure board container grid
        for i in range(3):
            self.board_container.grid_columnconfigure(i, weight=1)
            self.board_container.grid_rowconfigure(i, weight=1)
        
        # Create game board
        self.create_board()
        
        # Create reset button container
        self.button_container = tk.Frame(self.window, bg='#f0f0f0')
        self.button_container.grid(row=5, column=0, columnspan=3, sticky="ew", padx=20, pady=20)
        self.button_container.grid_columnconfigure(0, weight=1)
        
        # Create reset button
        self.reset_button = tk.Button(
            self.button_container,
            text="Nuova Partita",
            font=('Helvetica', 12),
            command=self.reset_game,
            bg='#4CAF50',
            fg='white',
            padx=20,
            pady=10
        )
        self.reset_button.grid(row=0, column=0)
        
        # Set minimum window size
        self.window.update_idletasks()
        min_width = 400
        min_height = 500
        self.window.minsize(min_width, min_height)
        
        # Center window
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - min_width) // 2
        y = (screen_height - min_height) // 2
        self.window.geometry(f'{min_width}x{min_height}+{x}+{y}')
        
        # Bind resize event
        self.window.bind('<Configure>', self.on_window_resize)

    def create_board(self):
        """Create the game board buttons."""
        for i in range(3):
            for j in range(3):
                button = tk.Button(
                    self.board_container,
                    text="",
                    font=('Helvetica', 20, 'bold'),
                    command=lambda row=i, col=j: self.make_move(row, col),
                    bg='#ffffff',
                    fg='#333333'
                )
                button.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                self.buttons[i][j] = button

    def on_window_resize(self, event):
        """Handle window resize events."""
        # Update button sizes based on window size
        if event.widget == self.window:
            # Calculate button size based on window size
            button_size = min(
                (event.width - 40) // 3,  # Width-based size
                (event.height - 200) // 3  # Height-based size
            )
            
            # Update button sizes
            for i in range(3):
                for j in range(3):
                    self.buttons[i][j].config(width=button_size//20, height=button_size//40)

    def make_move(self, row: int, col: int):
        """Handle a player's move."""
        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(
                text=self.current_player,
                fg='#e74c3c' if self.current_player == 'X' else '#3498db'
            )
            
            if self.check_winner():
                messagebox.showinfo("Fine del gioco", f"Il giocatore {self.current_player} ha vinto!")
                self.disable_board()
            elif self.is_board_full():
                messagebox.showinfo("Fine del gioco", "Pareggio!")
                self.disable_board()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.turn_label.config(text=f"Turno del giocatore: {self.current_player}")

    def check_winner(self) -> bool:
        """Check if there's a winner."""
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != " ":
                return True
        
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                return True
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return True
        
        return False

    def is_board_full(self) -> bool:
        """Check if the board is full."""
        return all(cell != " " for row in self.board for cell in row)

    def disable_board(self):
        """Disable all buttons after game end."""
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state='disabled')

    def reset_game(self):
        """Reset the game state."""
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.turn_label.config(text="Turno del giocatore: X")
        
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(
                    text="",
                    state='normal',
                    fg='#333333'
                )

    def run(self):
        """Start the game."""
        self.window.mainloop()

if __name__ == "__main__":
    game = TrisGUI()
    game.run() 