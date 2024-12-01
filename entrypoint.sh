#!/bin/bash
set -e

# Install dependencies
pip install --user -r requirements.txt

# Run the Python script
xvfb-run python get_auth_headers.py

# Exit the container
exit 0