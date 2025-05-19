# Use Python slim image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy everything to container
COPY . .

# Install Flask
RUN pip install --no-cache-dir flask

# Expose port 5000
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
