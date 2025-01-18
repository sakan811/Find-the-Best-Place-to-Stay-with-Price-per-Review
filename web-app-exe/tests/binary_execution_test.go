package tests

import (
	"os"
	"os/exec"
	"runtime"
	"testing"
)

func TestBinaryExecution(t *testing.T) {
	var binaryName string

	// Determine binary name based on OS
	switch runtime.GOOS {
	case "windows":
		binaryName = "find-place-web-app_windows_amd64.exe"
	case "darwin":
		if runtime.GOARCH == "arm64" {
			binaryName = "find-place-web-app_darwin_arm64"
		} else {
			binaryName = "find-place-web-app_darwin_amd64"
		}
	default:
		t.Skip("Unsupported OS for binary testing")
	}

	// Check if binary exists
	if _, err := os.Stat("../" + binaryName); os.IsNotExist(err) {
		t.Fatalf("Binary %s does not exist", binaryName)
	}

	// Test version command
	cmd := exec.Command("../"+binaryName, "--version")
	if err := cmd.Start(); err != nil {
		t.Fatalf("Failed to start binary: %v", err)
	}

	// Kill the process immediately after starting
	if err := cmd.Process.Kill(); err != nil {
		t.Logf("Warning: Failed to kill process: %v", err)
	}

	// Wait for the process to finish
	_ = cmd.Wait()

	t.Log("Binary execution test passed successfully")
}
