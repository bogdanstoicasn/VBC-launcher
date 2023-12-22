# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Upgrade pip to the latest version
RUN pip install --no-cache-dir --upgrade pip

# Create a writable directory for font cache
RUN mkdir -p /var/cache/fontconfig && chmod 777 /var/cache/fontconfig

# Copy all files from the current directory into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Specify the command to run on container start
CMD ["python", "vbc-launcher.py"]
