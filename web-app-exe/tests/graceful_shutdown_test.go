package tests

import (
	"os"
	"os/exec"
	"path/filepath"
	"testing"
)

func TestGracefulShutdown(t *testing.T) {
	// Create a temporary directory for testing
	tmpDir, err := os.MkdirTemp("", "test")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Set up test environment
	execDir = tmpDir

	// Create docker-compose.yml
	if err := os.WriteFile(filepath.Join(tmpDir, composeFile), []byte("version: '3'\n"), 0644); err != nil {
		t.Fatalf("Failed to create docker-compose.yml: %v", err)
	}

	// Save original execCommand and restore after
	originalExecCommand := execCommand
	defer func() { execCommand = originalExecCommand }()

	var cmdExecuted bool
	execCommand = func(name string, args ...string) *exec.Cmd {
		if name == "docker-compose" && len(args) > 0 && args[len(args)-1] == "down" {
			cmdExecuted = true
		}
		return exec.Command("true")
	}

	// Run gracefulShutdown
	gracefulShutdown()

	// Verify docker-compose down was called
	if !cmdExecuted {
		t.Error("Docker compose down command was not executed")
	}
}
