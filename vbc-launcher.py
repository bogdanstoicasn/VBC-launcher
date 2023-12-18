import tkinter as tkinter
from tkinter import ttk
from screeninfo import get_monitors
from datetime import datetime
import os
from PIL import Image, ImageTk

# Creation of child window
def enter_game(game, window):
    mode = tkinter.Toplevel(window)
    mode.title(game)
    message = "You have entered " + game + "!"
    label = tkinter.Label(mode, text=message)
    label.pack()
    second_label = tkinter.Label(mode, text="Coming soon!")
    second_label.pack()

# Centers the position of the window
def window_position(width, height, window):
    monitors = get_monitors()
    if monitors:
        primary_monitor = monitors[0]
        screen_width = primary_monitor.width
        screen_height = primary_monitor.height

    width = min(width, screen_width)
    height = min(height, screen_height)

    screen_width = (screen_width - width) // 2
    screen_height = (screen_height - height) // 2
    return width, height, screen_width, screen_height

# Display current time
def update_clock(label):
    current_time = datetime.now().strftime("%H:%M:%S")
    label.config(text=current_time)
    label.after(1000, lambda: update_clock(label))

# Modify for our games
game_array = ["Snake", "Sudoku", "Dice Game", "Asteroids"]
# Modify for our games


# Main function
def main():
    # get current folder path
    current_path = os.path.dirname(os.path.realpath(__file__))

    # Creation of the main window
    window = tkinter.Tk()
    window.title("VBC-LAUNCHER")
    window.resizable(False, False)

    # Position of the window on the screen
    x_offset, y_offset, screen_width, screen_height = window_position(400, 400, window)
    window.geometry(f"{x_offset}x{y_offset}+{screen_width}+{screen_height}")
    window.configure(bg="#5D3FD3")

    welcome_text = tkinter.Label(
        window,
        text="Welcome to VBC!",
        font=("Lato", 24, "bold", "italic"),
        fg="#E2DFD2",  # Text color
        bg="#5D3FD3"
    )
    welcome_text.pack(side="top", pady=(0, 20))

    clock_label = tkinter.Label(window, text="", font=("Arial", 10), bg="#5D3FD3", fg="#E2DFD2")
    clock_label.pack(side="bottom", anchor="se", padx=10, pady=10)

    update_clock(clock_label)


    frame = tkinter.Frame(window, bg="#5D3FD3")
    frame.pack()

    frame = tkinter.Frame(window, bg="#5D3FD3")
    frame.pack(pady=10)

    for i, game in enumerate(game_array):
        image_path = current_path + "/images/" + game + ".jpg"

        # Open the image using Pillow
        img = Image.open(image_path)
        button_size = (75, 75)  # Adjust the size as needed
        img = img.resize(button_size)

        # Convert the image to Tkinter PhotoImage
        img = ImageTk.PhotoImage(img)
        # Assign the game to the button
        button = tkinter.Button(
            frame,
            command=lambda t=game: enter_game(game, window),
            image=img,
            text=game,
            borderwidth=5,  # Remove border
            bg="#5D3FD3",  # Background color
            fg="#5D3FD3",  # Text color
            highlightthickness=0,  # Remove highlight
            activebackground="#E2DFD2",  # Background color when clicked
        )
        button.image = img  # Keep a reference to the image to prevent garbage collection
        button.grid(row=i // 2, column=i % 2, sticky="ew", padx=10, pady=5)

    exit_button = tkinter.Button(
        window,
        text="Exit",
        command=window.destroy,
        bg="#D22B2B",  # Background color
        fg="#E2DFD2",  # Text color
        font=("Arial", 12),
        padx=10,
        pady=5,
        bd=5,  # Border width
        relief=tkinter.RAISED,  # Border style
        highlightbackground="#5D3FD3",
        highlightthickness=5,
    )
    exit_button.pack(side="bottom")

    window.mainloop()

if __name__ == "__main__":
    main()
