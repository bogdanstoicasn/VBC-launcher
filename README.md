# VBC-launcher
Game launcher in python.

# Build and Run

docker build -t your_image_name .

<code>
docker run -u=$(id -u $USER):$(id -g $USER) -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:rw -v $(pwd):/app --rm your_image_name
</code>

*FOR BEST EXPERIENCE DON'T USE DOCKER, INSTEAD do:*

    sudo apt install python3

    
    pip install easygui

# Contributors

[![GitHub contributors](https://img.shields.io/github/contributors/yourusername/yourrepository.svg)](https://github.com/yourusername/yourrepository/graphs/contributors)

