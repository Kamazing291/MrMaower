# Use the official stable 3.14 image
FROM python:3.14-slim

# Fix for the "No address associated with hostname" error
# This installs the root certificates needed to trust Discord's SSL/DNS
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install your bot's requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files (including assets/)
COPY . .

# Force logs to show up instantly on Hugging Face
ENV PYTHONUNBUFFERED=1

# Start the bot
CMD ["python", "main.py"]
