# VBC-launcher
Game launcher in python.

# Build and Run

docker build -t your_image_name .

``docker run -u=$(id -u $USER):$(id -g $USER) -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:rw -v /home/bogdan/git/VBC-launcher:/app --rm your_image_name

