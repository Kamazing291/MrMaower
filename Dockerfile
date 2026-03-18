# Use the official Python 3.14 slim image for 2026
FROM python:3.14-slim

# Set the working directory
WORKDIR /app

# Copy your requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your bot's code
COPY . .

# Start the bot
CMD ["python", "main.py"]