#!/bin/bash

# Function to stop the servers
cleanup() {
  echo "Stopping servers..."
  kill $DJANGO_PID
  kill $REACT_PID
  exit 0
}

# Trap the termination signals (Ctrl+C)
trap cleanup SIGINT SIGTERM

# Navigate to the backend directory and start the Django server
cd backend || { echo "Backend directory not found"; exit 1; }
echo "Starting Django server..."
python manage.py runserver &

# Capture the PID of the Django server to kill it later if needed
DJANGO_PID=$!

# Navigate to the frontend directory and start the React server
cd ../frontend || { echo "Frontend directory not found"; kill $DJANGO_PID; exit 1; }
echo "Starting React server..."
npm start &

# Capture the PID of the React server to kill it later if needed
REACT_PID=$!

# Wait for the React server to start by checking the availability of localhost:3000
echo "Waiting for React server to start..."
until curl -s http://localhost:3000 > /dev/null; do
  sleep 1
done

# Wait for both servers to exit
wait $DJANGO_PID
wait $REACT_PID
