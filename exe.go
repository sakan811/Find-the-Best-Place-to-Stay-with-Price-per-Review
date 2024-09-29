package main

import (
	"fmt"
	"os"
	"os/exec"
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

	// Run docker-compose in detached mode (-d flag)
	cmd := exec.Command("docker", "compose", "up", "-d")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	cmd.Dir = "./"

	err := cmd.Run()
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		waitForUser() // Keeps the terminal open
		os.Exit(1)
	}

	fmt.Println("Please navigate to \033[34mhttp://localhost:5000/\033[0m to access the web-app.")

	fmt.Println("Docker containers are running in detached mode.")
	waitForUser() // Wait for the user before closing the terminal
}
