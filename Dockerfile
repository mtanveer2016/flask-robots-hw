# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for GPIO
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY templates/ ./templates/
COPY static/ ./static/

# Expose port
EXPOSE 5005

# Run the application
CMD ["python", "app.py"]