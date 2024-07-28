#!/bin/bash

# Function to create a virtual environment and install Python dependencies
setup_backend() {
    cd backend || exit

    # Create a new virtual environment
    python -m venv venv

    # Activate the virtual environment based on the operating system
    if [[ "$OSTYPE" == "msys" ]]; then
        # For Windows
        source venv/Scripts/activate
    elif [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
        # For Unix-based systems (Linux and macOS)
        source venv/bin/activate
    else
        echo "Unsupported operating system"
        exit 1
    fi

    # Install all dependencies listed in requirements.txt
    pip install -r requirements.txt

    # Create a .env file inside the backend directory with the specified variables
    cat <<EOL > .env
USER_AGENT=
EOL

    # Navigate back to the root directory
    cd .. || exit
}

# Function to install Node.js dependencies for the frontend
setup_frontend() {
    cd frontend || exit

    # Run npm install
    npm install

    # Navigate back to the root directory
    cd .. || exit
}

# Check the operating system and run the appropriate setup steps
if [[ "$OSTYPE" == "msys" ]]; then
    echo "Detected Windows OS"
    setup_backend
    setup_frontend
elif [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    echo "Detected Unix-based OS (Linux or macOS)"
    setup_backend
    setup_frontend
else
    echo "Unsupported operating system"
    exit 1
fi

echo "Setup complete!"
