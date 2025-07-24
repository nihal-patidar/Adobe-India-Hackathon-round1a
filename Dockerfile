# Use a slim Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpoppler-cpp-dev \
    pkg-config \
    python3-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements into the image
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Run the main script
CMD ["python", "main.py"]
