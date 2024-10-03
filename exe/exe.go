package main

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
)

// checkDockerRunning checks if Docker is running
func checkDockerRunning() bool {
	cmd := exec.Command("docker", "info")
	err := cmd.Run()
	return err == nil // Return true if no error, meaning Docker is running
}

func waitForUser() {
	fmt.Println("Press 'Enter' to exit...")
	fmt.Scanln() // Wait for user input
}

func main() {
	// Check if Docker is running
	if !checkDockerRunning() {
		fmt.Println("Error: Docker is not running. Please start Docker Desktop.")
		waitForUser() // Keeps the terminal open
		os.Exit(1)
	}

	// Get the directory of the executable
	exePath, err := os.Executable()
	if err != nil {
		fmt.Printf("Error getting executable path: %v\n", err)
		waitForUser()
		os.Exit(1)
	}
	exeDir := filepath.Dir(exePath)

	// Change to the directory of the executable
	err = os.Chdir(exeDir)
	if err != nil {
		fmt.Printf("Error changing to executable directory: %v\n", err)
		waitForUser()
		os.Exit(1)
	}

	// Run docker-compose in detached mode (-d flag)
	cmd := exec.Command("docker", "compose", "up", "-d")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err = cmd.Run()
	if err != nil {
		fmt.Printf("Error running Docker Compose: %v\n", err)
		waitForUser()
		os.Exit(1)
	}

	fmt.Println("Please navigate to \033[34mhttp://localhost:5000/\033[0m to access the web-app.")
	fmt.Println("Docker containers are running in detached mode.")
	waitForUser() // Wait for the user before closing the terminal
}
