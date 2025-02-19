# Dockerfile for user-service

# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Set the python execution
ENV PYTHONPATH="/app"

# Copy the requirements file
COPY ./requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app.py
COPY . .

# Expose the port the app runs on
EXPOSE 7070

# Command to run the application
CMD ["python", "app.py"]