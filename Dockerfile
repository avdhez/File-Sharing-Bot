FROM python:3.8-slim-buster

WORKDIR /app

# Install build-essential and other dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev

# Upgrade pip
RUN pip3 install --upgrade pip

# Copy and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir --verbose

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["python3", "main.py"]
