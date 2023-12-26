import tkinter as tk
from tkinter import font
from random import randint
from PIL import Image, ImageTk

class Die:
    def __init__(self):
        self.sides = 6
        self.roll_result = 0

    def roll(self):
        self.roll_result = randint(1, 6)

    def print_result(self):
        if self.roll_result == 0:
            return "Roll the dice first!"
        else:
            return "You have rolled " + str(self.roll_result)

class DiceWindow(tk.Toplevel):
    
    def __init__(self):
        super().__init__()
        self.title("Dice Game!")
        self.geometry("400x300")
        self.configure(bg="#000080")
        self.dice = Die()
        self.destroyed = False  # Flag to track if the window is destroyed

    def configDisplay(self):
        display_frame = tk.Frame(master=self, background="#000080")
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Roll the dice!",
            font=font.Font(size=20, weight="bold"),
            background="#000080",
            foreground="#FFFF00",
        )
        self.display.pack()

    def atRoll(self, T, image_label):
        self.dice.roll()
        result_text = self.dice.print_result()

        # clear old text on new roll and reinitialise 
        T.delete("1.0", "end")
        T.insert(tk.END, "Let's see what you will get..\n")
        self.animate_dice_roll(image_label, T, result_text, 0)

    def animate_dice_roll(self, image_label, T, result_text, frame):

        # display 10 frames from my gif
        if frame < 10:  
            self.display_gif_frame(image_label, frame)
            frame += 1

            # wait inbetweenframes 100 ms
            self.after(100, lambda: self.animate_dice_roll(image_label, T, result_text, frame))
        else:

            # add the rolling result
            T.insert(tk.END, result_text + "!\n")
            self.display_image(image_label, self.dice.roll_result)

    def display_gif_frame(self, image_label, frame):

        gif_img = Image.open("images/dice images/dice-roll-the-dice.gif")

        # get frame from source gif
        gif_img.seek(frame)
        gif_img = gif_img.resize((100, 100))
        frame_img = ImageTk.PhotoImage(gif_img)
        image_label.config(image=frame_img)
        image_label.image = frame_img

    def display_image(self, image_label, index):

        image_path = "images/dice images/" + str(index) + ".png"
        img = Image.open(image_path)
        img = img.resize((100, 100))
        img = ImageTk.PhotoImage(img)
        image_label.config(image=img)

        # save image to avoid deletion while running
        image_label.image = img

    def rolling(self):
        self.configDisplay()

        T = tk.Text(self, height=5, width=50)
        T.pack()

        T.insert(tk.END, "Let's see what you will get..\n")

        # Image label
        image_label = tk.Label(self, background = "#000080")
        image_label.pack()

        button = tk.Button(self, text="Roll!",bg = "#FFFF00", command=lambda: self.atRoll(T, image_label))
        button.pack(side=tk.BOTTOM, pady=20)

        # Handle window closing
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        if not self.destroyed:
            self.destroy()

    def display_gif(self, image_label):
        gif_path = "images/dice images/dice-roll-the-dice.gif"
        gif_img = Image.open(gif_path)
        gif_img = gif_img.resize((100, 100))
        gif_img = ImageTk.PhotoImage(gif_img)
        image_label.config(image=gif_img)
        image_label.image = gif_img

def play_dice():
    window = DiceWindow()
    window.rolling()

if __name__ == "__main__":
    play_dice()
