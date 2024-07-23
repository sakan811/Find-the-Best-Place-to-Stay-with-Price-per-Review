#!/bin/bash

# Navigate to the backend directory
cd backend

# Create a new virtual environment
python -m venv venv

# Activate the virtual environment
if [ -f "venv/Scripts/activate" ]; then
    # For Windows
    source venv/Scripts/activate
elif [ -f "venv/bin/activate" ]; then
    # For Unix-based systems
    source venv/bin/activate
else
    echo "Failed to create virtual environment"
    exit 1
fi

# Install all dependencies listed in requirements.txt
pip install -r requirements.txt

# Create a .env file inside the backend directory with the specified variables
cat <<EOL > .env
USER_AGENT=
X_BOOKING_CSRF_TOKEN=
X_BOOKING_CONTEXT_ACTION_NAME=
X_BOOKING_CONTEXT_AID=
X_BOOKING_ET_SERIALIZED_STATE=
X_BOOKING_PAGEVIEW_ID=
X_BOOKING_SITE_TYPE_ID=
X_BOOKING_TOPIC=
EOL

# Navigate to the frontend directory
cd ../frontend

# Run npm install
npm install

echo "Setup complete!"
