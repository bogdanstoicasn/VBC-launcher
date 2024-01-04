# VBC-launcher
A simple game launcher written in Python using Tkinter and Pygame. Launch your favorite games with a click!

### Our Team

- **Stoica Mihai-Bogdan 325CA**
- **Vulpe Cezar-Andrei 325CA**
- **Muntean Vlad-Andrei 325CA**

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

6. **Worlde**
    - A game with words

## Requirements

- Python 3.10 or above
- Tkinter (usually included with Python installation)
- easygui (install using `pip install easygui`)
- Pygame 2.5.2 (install using `pip install pygame`)

## Build and Run

### Clone the repository:

1. Clone the repository:

    git clone https://github.com/bogdanstoicasn/VBC-launcher.git

2. Navigate to the project directory:

    cd VBC-launcher


### Docker(not recommended - LINUX ONLY):

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

Install pygame:

    Step 3.3: pip install pygame

Install Tkinter:

    Step 3.3: sudo apt-get install python3-tk

Install screeninfo:

    Step 3.4: pip install screeninfo

Upgrade pip and pillow:

    Step 3.5: pip install --upgrade pip

    Step 3.6: pip install --upgrade pillow

3. Run the launcher:

    `python3 vbc-launcher.py`

## Usage of the launcher

+ Click on the game icons to launch the corresponding games.

+ Click on the "Exit" button to close the launcher.

+ Click on "Open File Explorer" to access your files directly from the
launcher(can run excutables/Python scripts).


## Contributors

**Bogdan**:

- Created launcher app
- Built Tic-tac-toe and Sudoku games
- Fixed bugs for platform compatibility and docker
- Challenges met: getting used to the **tkinter** interface and reduced number of widgets + developing the Sudoku generation algorithm
- Solutions: Generating the table line by line with verifications at each step. If verification fails, the line is regenerated


**Cezar**:

- Developed Asteroids and Wordle games
- Fixed bugs for launcher integration
- Challenges met: Familiarizing with the Pygame library and resolving the *"bullet not in list"* error for multiple collisions in the Asteroids game + optimising performance of Asteroids.
- Solutions: Check if bullet is in list + deleting entities that go offscreen


**Vlad**:

- Developed Dice Game and Snake Game
- Fixed display bugs and system compatibility issues
- Challenges met: Familiarizing with the Pygame library, every time the *run_snake* function was imported in launcher, generating and empty Pygame window + making a graphic selection screen for Snake skins + making the rolling hand GIF play in Dice Game
- Solutions: Encapsulated the pygame initialisation and window creation in the *run_snake* command to generate a new window every run + generating a triangle that moves to the center of the selected text for the snake's skin + rendering the GIF's frame one at a time

### Resources

->[pygame](https://www.pygame.org/news)

->[tkinter](https://docs.python.org/3/library/tkinter.html)


### Statistics


[![GitHub contributors](https://img.shields.io/github/contributors/bogdanstoicasn/VBC-launcher.svg)](https://github.com/bogdanstoicasn/VBC-launcher/graphs/contributors)

