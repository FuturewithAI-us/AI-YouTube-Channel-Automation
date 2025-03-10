# Use an official Python runtime
FROM python:3.8-slim

# Set working directory in the container
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Default command (can be modified later for different agents)
CMD ["python", "content_research_agent.py"]
