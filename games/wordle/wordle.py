import tkinter as tk
from tkinter import messagebox
import random
import os
from PIL import Image, ImageTk

class WordleGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Wordle Game")
        self.rows = 6
        self.columns = 5
        self.current_row = 0
        self.current_column = 0
        self.word_to_guess = ""
        self.guesses = [['' for _ in range(self.columns)] for _ in range(self.rows)]
        self.score_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "images", "asteroids images", "score.txt")
        self.hints_taken = 0
        self.hint_letters_taken = []

        self.master.geometry(f"{root.winfo_reqwidth() * 2}x{root.winfo_reqheight() * 2}")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        words_file_path = os.path.join(script_dir, "..", "..", "images", "asteroids images", "wordle-words.txt")

        if os.path.exists(words_file_path):
            self.word_to_guess = random.choice(self.load_words())
        else:
            messagebox.showerror("Error", f"File {words_file_path} not found!")

        image_path = os.path.join(script_dir, "..", "..", "images", "asteroids images", "wordle.png")

        if os.path.exists(image_path):
            original_image = Image.open(image_path)
            resized_image = original_image.resize((original_image.width // 3, original_image.height // 3))
            self.image = ImageTk.PhotoImage(resized_image)

            canvas = tk.Canvas(self.master, width=self.image.width(), height=self.image.height())
            canvas.pack()

            canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
        else:
            messagebox.showerror("Error", f"Image {image_path} not found!")

        self.create_widgets()
        self.load_score()

        # Adaugă butonul pentru a primi un indiciu
        hint_button = tk.Button(self.master, text="Get Hint", command=self.get_hint)
        hint_button.pack()

    def create_widgets(self):
        self.frames = []
        for row in range(self.rows):
            frame = tk.Frame(self.master)
            frame.pack(side=tk.TOP)
            self.frames.append(frame)

            for col in range(self.columns):
                entry_var = tk.StringVar()
                entry = tk.Entry(frame, textvariable=entry_var, width=8)
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
        if all(self.guesses[row]):
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
                messagebox.showinfo("Congratulations", "You guessed the word!")
                self.update_score()
                self.reset_game()
            else:
                if row == self.rows - 1:
                    messagebox.showinfo("Game Over", f"The correct word was: {self.word_to_guess}")
                    self.reset_game()

    def color_entry(self, row, col, color):
        frame = self.frames[row]
        entry_widgets = frame.winfo_children()

        entry = entry_widgets[col]
        entry.configure({"background": color})

    def load_score(self):
        if os.path.exists(self.score_file_path):
            with open(self.score_file_path, 'r') as file:
                try:
                    self.score = int(file.read())
                except ValueError:
                    messagebox.showwarning("Warning", "Score file content is not valid.")
                    self.score = 0
        else:
            self.score = 0

    def update_score(self):
        self.score += 1
        with open(self.score_file_path, 'w') as file:
            file.write(str(self.score))
        messagebox.showinfo("Score Updated", f"Your score is now: {self.score}")

    def reset_game(self):
        for frame in self.frames:
            frame.destroy()
        self.current_row = 0
        self.current_column = 0
        self.word_to_guess = random.choice(self.load_words())
        self.guesses = [['' for _ in range(self.columns)] for _ in range(self.rows)]
        self.hints_taken = 0
        self.hint_letters_taken = []
        self.create_widgets()

    def get_hint(self):
        if self.hints_taken >= 5:
            messagebox.showinfo("Max Hints Taken", f"You already know all the letters: {', '.join(self.hint_letters_taken)}.")
            return

        if self.score < 1:
            messagebox.showinfo("Hint Unavailable", "You don't have enough points to get a hint.")
            return

        self.score -= 1
        self.hints_taken += 1

        # Obține o literă diferită față de cele deja obținute
        remaining_letters = list(self.word_to_guess)

        for letter in self.hint_letters_taken:
            if letter in remaining_letters:
                remaining_letters.remove(letter)

        hint_letter = random.choice([l for l in remaining_letters])

        # Adaugă litera la lista de litere obținute prin hint-uri
        self.hint_letters_taken.append(hint_letter)
        # Afișează litera obținută prin hint
        messagebox.showinfo("Hint", f"The word contains the letter '{hint_letter}'.")
        self.score = self.score - 1 
        self.update_score()
    

    def load_words(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        words_file_path = os.path.join(script_dir, "..", "..", "images", "asteroids images", "wordle-words.txt")
        if os.path.exists(words_file_path):
            with open(words_file_path, 'r') as file:
                return file.read().splitlines()
        else:
            messagebox.showerror("Error", f"File {words_file_path} not found!")

if __name__ == "__main__":
    root = tk.Tk()
    game = WordleGame(root)
    root.mainloop()
