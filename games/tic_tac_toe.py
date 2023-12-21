# Tic-Tac-Toe Game
import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import NamedTuple


class Player(NamedTuple):
    label: str
    color: str


class Move(NamedTuple):
    row: int
    col: int
    label: str = ""


BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label="X", color="black"),
    Player(label="O", color="red"),
)


class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self.current_moves = []
        self._has_winner = False
        self.winning_combos = []
        self.games_played = 0 # games played
        self.x_wins = 0 # x wins
        self.o_wins = 0
        self.setup_board()

    def setup_board(self):
        self.current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self.winning_combos = self.get_winning_combos()

    def reset_game(self):
    # Reset the game state to play again.
        self.current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._has_winner = False
        self.winner_combo = []
        self.games_played += 1

    def get_winning_combos(self):
        rows = [[(move.row, move.col) for move in row] for row in self.current_moves]
        columns = [[(move.row, move.col) for move in row] for row in zip(*self.current_moves)]
        first_diagonal = [(i, i) for i in range(len(self.current_moves))]
        second_diagonal = [(i, len(self.current_moves) - 1 - i) for i in range(len(self.current_moves))]

        return rows + columns + [first_diagonal, second_diagonal]

    def process_move(self, move):
        # Process the current move and check if it's a win.
        row, col = move.row, move.col
        self.current_moves[row][col] = move
        for combo in self.winning_combos:
            results = set(self.current_moves[n][m].label for n, m in combo)
            if (len(results) == 1) and ("" not in results):
                self._has_winner = True
                self.winner_combo = combo
                if results.pop() == "X":
                    self.x_wins += 1
                else:
                    self.o_wins += 1
                break

    def is_valid_move(self, move):
        return not self._has_winner and self.current_moves[move.row][move.col].label == ""

    def has_winner(self):
        # Return True if the game has a winner, and False otherwise.
        return self._has_winner

    def is_tied(self):
        # Return True if the game is tied, and False otherwise.
        no_winner = not self._has_winner
        played_moves = (
            move.label for row in self.current_moves for move in row
        )
        return no_winner and all(played_moves)

    def toggle_player(self):
        # Return a toggled player.
        self.current_player = next(self._players)



class TicTacToeBoard(tk.Toplevel):
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self.resizable(False, False)
        self.geometry("400x400")
        self._cells = {}
        self._game = game
        self.create_menu()
        self.create_board_display()
        self.create_board_grid()

    def create_menu(self):
        # Create the game's menu.
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="New game", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def create_board_display(self):
        # Create the game's display.
        display_frame = tk.Frame(master=self, background="#FFFFFF")
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready to play?",
            font=font.Font(size=20, weight="bold"),
            background="#FFFFFF",
        )
        self.display.pack()

    def create_board_grid(self):
        # Create the game's board grid.
        grid_frame = tk.Frame(master=self, bg="black")
        grid_frame.pack()
    
        self.rowconfigure(0, weight=1, minsize=50)
        self.columnconfigure(0, weight=1, minsize=75)
    
        self._cells = {(button := tk.Button(
            master=grid_frame,
            text="",
            font=font.Font(size=36, weight="bold"),
            fg="#FFFFFF",
            bg="#FFFFFF",
            width=3,
            height=2,
            highlightbackground="#000000",
            highlightthickness=0,
        )): (row, col) for row in range(self._game.board_size) for col in range(self._game.board_size)}
    
        for button, (row, col) in self._cells.items():
            button.bind("<ButtonPress-1>", self.play)
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")


    def play(self, event):
        # Handle a player's move.
        row, col = self._cells[event.widget]
        move = Move(row, col, self._game.current_player.label)

        if self._game.is_valid_move(move):
            self.update_button(event.widget)
            self._game.process_move(move)

            if self._game.is_tied():
                self.update_display(msg="Tied game!", color="red")
            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'Player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self.update_display(msg, color)
            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self.update_display(msg)

    def update_display(self, msg, color="black"):
        # Update the game's display.
        font_size = 15
        self.display["text"] = msg
        self.display["fg"] = color
        self.display["font"] = font.Font(size=font_size, weight="bold")

    def update_button(self, clicked_button):
        # Update the clicked button.
        clicked_button.config(text=self._game.current_player.label)
        clicked_button.config(fg=self._game.current_player.color)

    def _highlight_cells(self):
        # Highlight the winning cells.
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="green", background="green")

    def reset_board(self):
        # Reset the game's board to play again.
        self._game.reset_game()
        self.update_display(msg="Games: " + str(self._game.games_played) + " | X Wins: " + str(self._game.x_wins) + " | O Wins: " + str(self._game.o_wins))
        for button in self._cells.keys():
            button.config(highlightbackground="#000000", background="#FFFFFF")
            button.config(text="")
            button.config(fg="black")

def play_tic_tac_toe():
    # Play a game of tic-tac-toe.
    game = TicTacToeGame()
    board = TicTacToeBoard(game)
    board.mainloop()

def main():
    # Create the game and run it.
    root = tk.Tk()
    root.withdraw()
    game = TicTacToeGame()
    board = TicTacToeBoard(game)

    # Close both windows when the Toplevel window is closed
    def on_closing():
        root.destroy()

    # Set up the closing protocol
    board.protocol("WM_DELETE_WINDOW", on_closing)

    # Start the game loop for the Toplevel window
    board.mainloop()


if __name__ == "__main__":
    main()