FROM python:3.14-slim

# 1. Install certificates
# 2. Force the OS to prefer IPv4 over IPv6
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates \
    && echo "precedence ::ffff:0:0/96 100" >> /etc/gai.conf \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]
