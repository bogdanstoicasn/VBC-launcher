import tkinter as tk
from tkinter import messagebox
import random

class WordleGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Wordle Game")
        self.rows = 6
        self.columns = 5
        self.current_row = 0
        self.current_column = 0
        self.word_to_guess = self.choose_word()
        self.guesses = [['' for _ in range(self.columns)] for _ in range(self.rows)]

        self.create_widgets()

    def choose_word(self):
        words = ["piton", "codig", "aaaaa", "wordl", "blend", "happy"]
        five_letter_words = [word for word in words if len(word) == 5]
        return random.choice(five_letter_words)

    def create_widgets(self):
        self.frames = []
        for row in range(self.rows):
            frame = tk.Frame(self.master)
            frame.pack(side=tk.TOP)
            self.frames.append(frame)

            for col in range(self.columns):
                entry_var = tk.StringVar()
                entry = tk.Entry(frame, textvariable=entry_var, width=4)
                entry.grid(row=row, column=col)
                entry.bind('<KeyPress>', lambda event, r=row, c=col: self.on_key_press(event, r, c))
                entry_var.trace_add('write', lambda *args, r=row, c=col, var=entry_var: self.on_var_change(r, c, var))
                entry.bind('<Return>', lambda event, r=row, c=col: self.check_result_on_cell(r, c))

    def on_key_press(self, event, row, column):
        char = event.char.lower()
        if char.isalpha() and len(char) == 1:
            self.guesses[row][column] = char
            self.move_to_next_cell()

    def on_var_change(self, row, column, var):
        value = var.get()
        if len(value) > 1:
            var.set(value[-1])
        self.guesses[row][column] = value
        self.move_to_next_cell()

    def move_to_next_cell(self):
        self.current_column += 1
        if self.current_column == self.columns:
            self.current_column = 0

        if self.current_row == self.rows:
            self.check_result()

    def check_result_on_cell(self, row, col):
        if all(self.guesses[row]):  # Verificați doar dacă rândul este completat
            for c, letter in enumerate(self.guesses[row]):
                correct_letter = self.word_to_guess[c]
                if letter == correct_letter:
                    self.color_entry(row, c, 'green')
                elif letter in self.word_to_guess:
                    self.color_entry(row, c, 'yellow')
                else:
                    self.color_entry(row, c, 'red')

            user_word = ''.join(self.guesses[row])
            if user_word == self.word_to_guess:
                messagebox.showinfo("Felicitări", "Ai ghicit cuvântul!")
            else:
                if row == self.rows - 1:  # Afișați cuvântul doar după ultimul rând
                    messagebox.showinfo("Sfârșit de joc", f"Cuvântul corect era: {self.word_to_guess}")

    def color_entry(self, row, col, color):
        frame = self.frames[row]
        entry_widgets = frame.winfo_children()

        entry = entry_widgets[col]
        entry.configure({"background": color})

if __name__ == "__main__":
    root = tk.Tk()
    game = WordleGame(root)
    root.mainloop()
