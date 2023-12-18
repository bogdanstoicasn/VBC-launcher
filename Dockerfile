# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Install XVFB
RUN apt-get update && apt-get install -y xvfb

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Start XVFB and run vbc-launcher.py when the container launches
CMD ["xvfb-run", "python", "./vbc-launcher.py"]

