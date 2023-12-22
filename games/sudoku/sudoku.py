import tkinter as tk
from tkinter import messagebox
import webbrowser

try:
    from games.sudoku.sudoku_generator import puzzle_generator
except ModuleNotFoundError:
    # This exception will occur if running the script individually
    # Handle the exception by using a relative import
    from sudoku_generator import puzzle_generator

class SudokuGUI(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Sudoku Game")
        self.geometry("365x305")  # Increased height for the mistakes label
        self.config(bg="#28282B")
        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set("beginner")

        self.mistakes = 0  # Initialize mistakes variable

        self.create_menu()
        self.create_board()
        self.create_mistakes_label()

    def create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        difficulty_menu = tk.Menu(menu_bar, tearoff=0)
        difficulty_menu.add_radiobutton(label="Beginner", variable=self.difficulty_var, value="beginner", command=self.new_game)
        difficulty_menu.add_radiobutton(label="Intermediate", variable=self.difficulty_var, value="intermediate", command=self.new_game)
        difficulty_menu.add_radiobutton(label="Advanced", variable=self.difficulty_var, value="advanced", command=self.new_game)

        menu_bar.add_cascade(label="Difficulty", menu=difficulty_menu)
        def open_url():
            webbrowser.open_new("https://www.wikihow.com/Solve-a-Sudoku")
        menu_bar.add_command(label="How to play", command=open_url)

    def create_board(self):
        self.solution, self.originMat = puzzle_generator(self.difficulty_var.get())
        self.board = [[tk.StringVar(value="" if self.solution[i][j] == 0 else str(self.solution[i][j])) for j in range(9)] for i in range(9)]
        self.entry_widgets = [[None] * 9 for _ in range(9)]  # To store Entry widgets

        for i in range(9):
            for j in range(9):
                padx = pady = 1

                if i % 3 == 0 and i > 0:
                    pady = (3, 0)
                if j % 3 == 0 and j > 0:
                    padx = (3, 0)
                if i == 0:
                    pady = (3, 0)
                if j == 0:
                    padx = (3, 0)
                if i == 8:
                    pady = (1, 3)
                if j == 8:
                    padx = (1, 3)
                entry = tk.Entry(self, textvariable=self.board[i][j], width=3, font=('Arial', 14), justify='center', bd=2)
                entry.grid(row=i, column=j, padx=padx, pady=pady)

                entry.bind('<KeyRelease>', lambda event, i=i, j=j: self.check_entry(event, i, j))
                entry.bind('<BackSpace>', lambda event, i=i, j=j: self.delete_entry(event, i, j))
                entry.bind('<Enter>', lambda event, i=i, j=j: self.highlight_row_and_column(i, j))
                entry.bind('<Leave>', lambda event, i=i, j=j: self.reset_highlight(i, j))
                self.entry_widgets[i][j] = entry  # Store the Entry widget

    def create_mistakes_label(self):
        self.mistakes_label = tk.Label(self, text="Mistakes: 0", font=('Arial', 12), bg="#28282B", fg="#FFFFFF")
        self.mistakes_label.grid(row=9, columnspan=9)

    def new_game(self):
        self.solution, self.originMat = puzzle_generator(self.difficulty_var.get())
        for i in range(9):
            for j in range(9):
                self.board[i][j].set("" if self.solution[i][j] == 0 else str(self.solution[i][j]))
                self.entry_widgets[i][j].config(bg="white")  # Reset background color
        self.mistakes = 0
        self.update_mistakes_label()

    def update_mistakes_label(self):
        self.mistakes_label.config(text=f"Mistakes: {self.mistakes}")

    def check_entry(self, event, i, j):
        try:
            entered_digit = int(self.board[i][j].get())
            if entered_digit != self.originMat[i][j]:
                self.mistakes += 1
                if self.mistakes == 3:
                    messagebox.showinfo("Game Over", "You've made 3 mistakes. Game over!")
                    self.new_game()
                else:
                    self.entry_widgets[i][j].config(bg="red")  # Set background color to red for mistaken digit
            else:
                self.entry_widgets[i][j].config(bg="white")  # Reset background color if correct digit
            self.update_mistakes_label()  # Update mistakes label
        except ValueError:
            pass  # Ignore non-integer inputs

    def delete_entry(self, event, i, j):
        self.entry_widgets[i][j].config(bg="white")  # Reset background color when deleting mistaken digit

    def highlight_row_and_column(self, i, j):
        for x in range(9):
            self.entry_widgets[x][j].config(bg="#D6D6D6")  # Highlight column
            self.entry_widgets[i][x].config(bg="#D6D6D6")  # Highlight row

    def reset_highlight(self, i, j):
        for x in range(9):
            self.entry_widgets[x][j].config(bg="white")  # Reset column highlight
            self.entry_widgets[i][x].config(bg="white")  # Reset row highlight

def play_sudoku():
    app = SudokuGUI()
    app.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = SudokuGUI()
    def on_closing():
        root.destroy()

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
