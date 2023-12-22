# VBC-launcher
A simple game launcher written in Python using Tkinter. Launch your favorite games with a click!

## Features

- Launch popular games with a single click.
- User-friendly GUI built with Tkinter.
- Clickable buttons for each game.
- Time and date display.

## Games Included

1. **Asteroids**
   - Classic arcade game where you navigate a spaceship and shoot asteroids.

2. **Dice**
   - Roll virtual dice and get random numbers.

3. **Sudoku**
   - Play the classic Sudoku puzzle game with varying difficulty levels.

4. **Tic Tac Toe**
   - Traditional Tic Tac Toe game for two players.

5. **Snake**
   - Control a snake to eat food and grow longer without hitting the walls.

## Requirements

- Python 3.6 or above
- Tkinter (usually included with Python installation)
- easygui (install using `pip install easygui`)

## Build and Run

1. Clone the repository:

>   git clone https://github.com/bogdanstoicasn/VBC-launcher.git

2. Navigate to the project directory:

>   cd VBC-launcher


### Docker(not recommended):

`Step 3.1: docker build -t your_image_name .`
<code>
Step 3.2: docker run -u=$(id -u $USER):$(id -g $USER) -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:rw -v $(pwd):/app --rm your_image_name
</code>

### Python(recommended):

Install python3:

    Step 3.1: sudo apt install python3

Install easygui:
    
    Step 3.2: pip install easygui

or

    Step 3.2: python3 -m pip install easygui

3. Run the launcher:

    `python3 vbc-launcher.py`

## Usage of the launcher

+ Click on the game icons to launch the corresponding games.

+ Click on the "Exit" button to close the launcher.

+ Click on "Open File Explorer" to access your files directly from the
launcher(can run excutables/Python scripts).


# Contributors

[![GitHub contributors](https://img.shields.io/github/contributors/yourusername/yourrepository.svg)](https://github.com/yourusername/yourrepository/graphs/contributors)

