# Use the official Python 3.12 slim image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Ensure logs show up instantly
ENV PYTHONUNBUFFERED=1

# Start the bot
CMD ["python", "main.py"]
