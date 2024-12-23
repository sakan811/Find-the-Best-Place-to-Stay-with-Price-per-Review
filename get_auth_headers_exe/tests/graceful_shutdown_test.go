package tests

import (
	"os"
	"os/exec"
	"path/filepath"
	"syscall"
	"testing"
	"time"
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
	mockCmd = &MockCmd{}

	// Save original and restore after
	originalExecCommand := execCommand
	defer func() { execCommand = originalExecCommand }()

	// Create docker-compose.yml
	if err := os.WriteFile(filepath.Join(tmpDir, composeFile), []byte("version: '3'\n"), 0644); err != nil {
		t.Fatalf("Failed to create docker-compose.yml: %v", err)
	}

	var cmdExecuted bool
	execCommand = func(name string, args ...string) *exec.Cmd {
		if name == "docker-compose" && len(args) > 0 && args[len(args)-1] == "down" {
			cmdExecuted = true
		}
		return exec.Command("true")
	}

	// Start graceful shutdown in a goroutine
	done := make(chan bool)
	go func() {
		gracefulShutdown()
		done <- true
	}()

	// Send interrupt signal
	proc, err := os.FindProcess(os.Getpid())
	if err != nil {
		t.Fatalf("Could not find process: %v", err)
	}

	// Send signal and wait for shutdown
	proc.Signal(syscall.SIGTERM)

	// Wait for shutdown or timeout
	select {
	case <-done:
		if !cmdExecuted {
			t.Error("Docker compose down command was not executed")
		}
	case <-time.After(2 * time.Second):
		t.Error("Graceful shutdown timed out")
	}
}
