# Base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the application files
COPY . .

# Install dependencies
RUN pip install --upgrade pip 

# Run tests (optional, but good for debugging)
RUN pytest tests/ || true

# Set the default command
CMD ["python", "main.py"]
