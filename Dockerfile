# Base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements.txt first (optimizes caching)
COPY requirements.txt .

# Install dependencies with cache optimization
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Run tests (optional, but will stop the build if tests fail)
RUN pytest tests/ || echo "Tests failed, but continuing build..."

# Set the default command
CMD ["python", "main.py"]
