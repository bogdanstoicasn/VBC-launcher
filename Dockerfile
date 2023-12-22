# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install required system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    apt-utils\
    tk \
    libgl1-mesa-glx \
    libx11-xcb1 \
    libxcb1 \
    libxext6 \
    libxrender1 \
    libxinerama1 \
    libfontconfig1 \
    libdbus-1-3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Install X11 utilities
RUN apt-get update && \
    apt-get install -y xauth && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the script and images into the container
COPY vbc-launcher.py /app/
COPY games /app/games
COPY images /app/images

# Run the GUI application
CMD ["python", "vbc-launcher.py"]
