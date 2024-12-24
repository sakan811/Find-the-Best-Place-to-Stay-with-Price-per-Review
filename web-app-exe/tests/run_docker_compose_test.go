package tests

import (
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"testing"
)

// MockCmd represents a mock command for testing
type MockCmd struct {
	executed bool
	args     []string
}

// Add at the top of the file
var execCommand = exec.Command

// Add at the top with other vars
var mockCmd *MockCmd

func TestRunDockerCompose(t *testing.T) {
	// Initialize mockCmd before using it
	mockCmd = &MockCmd{}

	// Create a temporary directory for testing
	tmpDir, err := os.MkdirTemp("", "test")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Set up test environment
	execDir = tmpDir

	tests := []struct {
		name          string
		setupFiles    bool
		expectError   bool
		errorContains string
	}{
		{
			name:          "Missing docker-compose.yml",
			setupFiles:    false,
			expectError:   true,
			errorContains: "docker-compose.yml file not found",
		},
		{
			name:        "Docker compose file exists",
			setupFiles:  true,
			expectError: false,
		},
	}

	// Save original and restore after
	originalExecCommand := execCommand
	defer func() { execCommand = originalExecCommand }()

	// Update the mock to use our variable
	execCommand = func(name string, args ...string) *exec.Cmd {
		mockCmd.executed = true
		mockCmd.args = append([]string{name}, args...)
		return exec.Command("true")
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Reset test directory
			os.RemoveAll(filepath.Join(tmpDir, composeFile))

			if tt.setupFiles {
				// Create docker-compose.yml
				if err := os.WriteFile(filepath.Join(tmpDir, composeFile), []byte("version: '3'\n"), 0644); err != nil {
					t.Fatalf("Failed to create docker-compose.yml: %v", err)
				}
			}

			// Run the test
			err := runDockerCompose()

			// Check error expectations
			if tt.expectError {
				if err == nil {
					t.Error("Expected an error but got none")
				} else if tt.errorContains != "" && !strings.Contains(err.Error(), tt.errorContains) {
					t.Errorf("Expected error containing %q, got %v", tt.errorContains, err)
				}
			} else {
				if err != nil {
					t.Errorf("Unexpected error: %v", err)
				}
			}
		})
	}
}
