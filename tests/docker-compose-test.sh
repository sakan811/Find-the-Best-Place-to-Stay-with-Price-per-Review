#!/bin/bash

# Function to clean up
cleanup() {
    echo "Cleaning up Docker Compose environment..."
    docker-compose down
    echo "Cleanup complete."
    exit 0
}

# Set up trap to catch SIGINT (Ctrl+C) and call cleanup
trap cleanup SIGINT

# Start Docker Compose in detached mode
echo "Starting Docker Compose in detached mode..."
docker-compose up -d

# Check if the container started successfully
if [ $? -ne 0 ]; then
    echo "Failed to start Docker Compose environment."
    exit 1
fi

echo "Docker Compose environment is up and running."
echo "Press Ctrl+C to stop and clean up when you're done."

# Wait indefinitely
while true; do
    sleep 1
done