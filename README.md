# VBC-launcher
Game launcher in python.

# Build and Run

Build = docker build -t vbc-launcher .

	xhost +local:docker

Run = docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix your-image-name


