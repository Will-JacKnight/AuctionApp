# Dockerfile for api-gateway

# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY ./requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app.py
COPY ./app.py .

# Expose the port the app runs on
EXPOSE 4000

# Command to run the application
CMD ["python", "app.py"]