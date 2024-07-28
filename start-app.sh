#!/bin/bash

# Function to stop the servers
cleanup() {
  echo "Stopping servers..."
  if [[ "$OSTYPE" == "msys" ]]; then
    # Windows
    taskkill //PID $DJANGO_PID //F 2>/dev/null || echo "Django server not running"
    taskkill //PID $REACT_PID //F 2>/dev/null || echo "React server not running"
  else
    # Unix-based systems
    kill $DJANGO_PID 2>/dev/null || echo "Django server not running"
    kill $REACT_PID 2>/dev/null || echo "React server not running"
  fi
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

# Check if the Django server started successfully
if ! kill -0 $DJANGO_PID > /dev/null 2>&1; then
  echo "Failed to start Django server"
  exit 1
fi

# Navigate to the frontend directory and start the React server
cd ../frontend || { echo "Frontend directory not found"; kill $DJANGO_PID; exit 1; }
echo "Starting React server..."
npm start &

# Capture the PID of the React server to kill it later if needed
REACT_PID=$!

# Check if the React server started successfully
if ! kill -0 $REACT_PID > /dev/null 2>&1; then
  echo "Failed to start React server"
  kill $DJANGO_PID
  exit 1
fi

# Wait for the React server to start by checking the availability of localhost:3000
echo "Waiting for React server to start..."
until curl -s http://localhost:3000 > /dev/null; do
  sleep 1
done

# Wait for both servers to exit
wait $DJANGO_PID
wait $REACT_PID
