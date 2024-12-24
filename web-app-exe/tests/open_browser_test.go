package tests

import (
	"os/exec"
	"testing"
)

func TestOpenBrowser(t *testing.T) {
	// Save original execCommand and restore after
	originalExecCommand := execCommand
	defer func() { execCommand = originalExecCommand }()

	tests := []struct {
		name          string
		goos          string
		url           string
		expectCommand string
		expectArgs    []string
		expectError   bool
	}{
		{
			name:          "Linux browser",
			goos:          "linux",
			url:           "http://localhost:8080",
			expectCommand: "xdg-open",
			expectArgs:    []string{"http://localhost:8080"},
			expectError:   false,
		},
		{
			name:          "Windows browser",
			goos:          "windows",
			url:           "http://localhost:8080",
			expectCommand: "rundll32",
			expectArgs:    []string{"url.dll,FileProtocolHandler", "http://localhost:8080"},
			expectError:   false,
		},
		{
			name:          "MacOS browser",
			goos:          "darwin",
			url:           "http://localhost:8080",
			expectCommand: "open",
			expectArgs:    []string{"http://localhost:8080"},
			expectError:   false,
		},
		{
			name:        "Unsupported platform",
			goos:        "unsupported",
			url:         "http://localhost:8080",
			expectError: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Save original GOOS and restore after test
			originalGOOS := goos
			goos = tt.goos
			defer func() { goos = originalGOOS }()

			var gotCommand string
			var gotArgs []string

			// Mock execCommand
			execCommand = func(name string, args ...string) *exec.Cmd {
				gotCommand = name
				gotArgs = args
				// Return a dummy successful command
				return exec.Command("true")
			}

			// Run the test
			err := openBrowser(tt.url)

			// Check error expectations
			if tt.expectError {
				if err == nil {
					t.Error("Expected an error but got none")
				} else if err.Error() != "unsupported platform" {
					t.Errorf("Expected 'unsupported platform' error, got: %v", err)
				}
				return
			}

			if err != nil {
				t.Errorf("Unexpected error: %v", err)
				return
			}

			// Verify command and arguments
			if gotCommand != tt.expectCommand {
				t.Errorf("Expected command %q, got %q", tt.expectCommand, gotCommand)
			}

			if len(gotArgs) != len(tt.expectArgs) {
				t.Errorf("Expected %d args, got %d", len(tt.expectArgs), len(gotArgs))
				return
			}

			for i, arg := range tt.expectArgs {
				if gotArgs[i] != arg {
					t.Errorf("Expected arg[%d]=%q, got %q", i, arg, gotArgs[i])
				}
			}
		})
	}
}
