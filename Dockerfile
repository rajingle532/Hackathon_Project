FROM python:3.10-slim

# Install system dependencies (Node.js for frontend/backend, and libgl1 for any ML image processing)
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs libgl1-mesa-glx libglib2.0-0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all project files into the container
COPY . .

# Make the startup script executable
RUN chmod +x start.sh

# Expose the single port that Hugging Face looks for
EXPOSE 7860

# Run all microservices together
CMD ["./start.sh"]
