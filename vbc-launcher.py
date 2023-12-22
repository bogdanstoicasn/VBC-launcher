import tkinter as tkinter
import easygui
from screeninfo import get_monitors
from datetime import datetime
import os
import sys
import subprocess
import functools
from PIL import Image, ImageTk

from games.tic_tac_toe import play_tic_tac_toe
from games.sudoku.sudoku import play_sudoku
# Creation of child window
def enter_game(game):
    match game:
        case "Tic-Tac-Toe":
             return play_tic_tac_toe()
        case "Snake":
            return print("Snake")
        case "Sudoku":
            return play_sudoku()
        case "Dice Game":
            return print("Dice Game")
        case "Asteroids":
            return print("Asteroids")
        case _:
            return print("Game not found")


# Centers the position of the window
def window_position(width, height):
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
    label.after(1000, lambda l=label: update_clock(l))
    
def run_selected_file(file_path):
    try:
        if file_path.endswith('.py') or os.access(file_path, os.X_OK):
            subprocess.run([sys.executable, os.path.abspath(file_path)], check=True)
        else:
            print("Selected file is not a Python script or executable.")
    except subprocess.CalledProcessError as e:
        print(f"Error opening file: {e}")

def open_file_explorer():
    try:
        # Open the file dialog to choose a file
        file_path = easygui.fileopenbox()

        # Check if a file was selected
        if file_path:
            # Run the selected file
            run_selected_file(file_path)

    except Exception as e:
        print(f"Error: {e}")


# Modify for our games
game_array = ["Snake", "Sudoku", "Dice Game", "Asteroids", "Tic-Tac-Toe"]
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
    x_offset, y_offset, screen_width, screen_height = window_position(400, 480)
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
    frame1 = tkinter.Frame(window, bg="#5D3FD3")
    clock_label = tkinter.Label(frame1, text="", font=("Arial", 10), bg="#5D3FD3", fg="#E2DFD2")
    clock_label.grid(row=0, column=1, sticky="e", padx=210, pady=5)
    launch_external_button = tkinter.Button(
        frame1,
        text="Open File Explorer",
        command=functools.partial(open_file_explorer),
        bg="#5D3FD3",  # Background color
        fg="#E2DFD2",  # Text color
        font=("Arial", 8, "underline"),
        padx=10,
        pady=5,
        highlightthickness=0,
        relief=tkinter.FLAT,
        activebackground="#5D3FD3",  # Background color when clicked
        activeforeground="#000000"
    )
    launch_external_button.grid(row=0, column=0, sticky="w", padx=5, pady=5)
    frame1.pack(side="bottom", anchor="center")

    update_clock(clock_label)


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

        # Get the function to call when the button is clicked
        function = enter_game
        # Assign the game to the button
        button = tkinter.Button(
            frame,
            command=functools.partial(function, game),
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
