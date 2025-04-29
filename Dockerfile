# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt first to leverage Docker cache for installing dependencies
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application files
COPY . /app/

# Expose the port for the app
EXPOSE 5000

# Run the application using gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
