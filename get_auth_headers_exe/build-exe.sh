#!/bin/bash

# Set the name of your Go application
APP_NAME="find-place-web-app"

# Change to the script's directory
cd "$(dirname "$0")" || exit

# Output current directory
echo "Building in $(pwd)"

# Build for Windows (64-bit)
echo "Building for Windows (64-bit)..."
GOOS=windows GOARCH=amd64 go build -o "${APP_NAME}_windows_amd64.exe" find_place_web_app.go

# Build for macOS (64-bit)
echo "Building for macOS (64-bit)..."
GOOS=darwin GOARCH=amd64 go build -o "${APP_NAME}_darwin_amd64" find_place_web_app.go

# Build for macOS (Apple Silicon)
echo "Building for macOS (Apple Silicon)..."
GOOS=darwin GOARCH=arm64 go build -o "${APP_NAME}_darwin_arm64" find_place_web_app.go

echo "Build complete!"