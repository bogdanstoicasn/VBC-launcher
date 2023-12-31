import tkinter as tkinter
import easygui
from datetime import datetime
import os
import sys
import subprocess
import functools
from PIL import Image, ImageTk
import webbrowser

from games.tic_tac_toe import play_tic_tac_toe
from games.sudoku.sudoku import play_sudoku
from games.dice import play_dice
from games.snake.snake import run_snake

# add here imports and the game running function
def enter_game(game):

    current_path = os.path.dirname(os.path.realpath(__file__))

    try:
        match game:
            case "Tic-Tac-Toe":
                return play_tic_tac_toe()
            case "Snake":
                return run_snake()
            case "Sudoku":
                return play_sudoku()
            case "Dice Game":
                return play_dice()
            case "Asteroids":
                subprocess.run(["python3", current_path + "/games/asteroizi/asteroizi.py"])
                return None
            case "Wordle":
                subprocess.run(["python3", current_path + "/games/wordle/wordle.py"])
                return print("Wordle")
            case "Info":
                return webbrowser.open("https://github.com/bogdanstoicasn/VBC-launcher")
            case _:
                return print("Game not found")

    except:
        if game == "Tic-Tac-Toe":
            return play_tic_tac_toe()
        elif game == "Snake":
            return run_snake()
        elif game == "Sudoku":
            return play_sudoku()
        elif game == "Dice Game":
            return play_dice()
        elif game == "Asteroids":
            subprocess.run(["python", current_path + "/games/asteroizi/asteroizi.py"])
            return None
        elif game == "Wordle":
            subprocess.run(["python", current_path + "/games/wordle/wordle.py"])
            return None
        elif game == "Info":
            return webbrowser.open("https://github.com/bogdanstoicasn/VBC-launcher")
        else:
            return print("Game not found")                         


# Centers the position of the window
def window_position(width, height):
    root = tkinter.Tk()
    root.attributes("-fullscreen", True)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

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

def launcher_icon(window):
    current_path = os.path.dirname(os.path.realpath(__file__))
    icon_path = current_path + "/images/icons/1.jpg"
    try:
    # Open the image with Pillow
        pil_image = Image.open(icon_path)

    # Resize the image to fit the icon size if needed
    # You can adjust the size based on your requirements
        pil_image = pil_image.resize((32, 32))

    # Convert the image to Tkinter format
        icon_image = ImageTk.PhotoImage(pil_image)

    # Set the window icon
        window.iconphoto(True, icon_image)
    except Exception as e:
    # Handle the error if the image file is not found or not supported
        print(f"Error loading icon: {e}, using default icon.")


# Modify for our games
game_array = ["Snake", "Sudoku", "Dice Game", "Asteroids", "Tic-Tac-Toe", "Wordle","Info"]
# Modify for our games


# Main function
def main():
    # get current folder path
    current_path = os.path.dirname(os.path.realpath(__file__))

    # Creation of the main window
    window = tkinter.Tk()
    window.title("VBC-LAUNCHER")
    window.resizable(False, False)
    launcher_icon(window)
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
        button_size = (70, 70)  # Adjust the size as needed
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
        if game == "Info":
            button.configure(relief=tkinter.GROOVE, activeforeground="#5D3FD3", activebackground="#E2DFD2")
            button.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
            continue
        button.image = img  # Keep a reference to the image to prevent garbage collection
        button.grid(row=i // 3, column=i % 3, sticky="ew", padx=10, pady=5)
    
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
