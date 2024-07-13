# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /backend

# Install dependencies
COPY requirements.txt /backend
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /backend

# Expose the port on which Django runs (typically 8000)
EXPOSE 8000

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
