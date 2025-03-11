# Use a more recent Python version for improved security and performance
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker caching
COPY requirements.txt ./

# Install system dependencies and Python packages
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Define the default command to run your application
CMD ["python", "main.py"]
