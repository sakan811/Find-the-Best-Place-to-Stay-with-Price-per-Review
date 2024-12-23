package tests

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestUpdateEnvFile(t *testing.T) {
	// Create a temporary directory for testing
	tmpDir, err := os.MkdirTemp("", "test")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Set up test environment
	execDir = tmpDir

	tests := []struct {
		name        string
		envExample  string
		envVars     map[string]string
		wantContent []string
	}{
		{
			name:       "Update existing variables",
			envExample: "USER_AGENT=example\nX_BOOKING_CLIENT_TYPE=test\n",
			envVars: map[string]string{
				"USER_AGENT":            "Mozilla/5.0",
				"X_BOOKING_CLIENT_TYPE": "browser",
			},
			wantContent: []string{
				"USER_AGENT=Mozilla/5.0",
				"X_BOOKING_CLIENT_TYPE=browser",
			},
		},
		{
			name:       "Preserve unmatched variables",
			envExample: "USER_AGENT=example\nOTHER_VAR=test\n",
			envVars: map[string]string{
				"USER_AGENT": "Mozilla/5.0",
			},
			wantContent: []string{
				"USER_AGENT=Mozilla/5.0",
				"OTHER_VAR=test",
			},
		},
		{
			name:       "Handle empty values",
			envExample: "USER_AGENT=example\n",
			envVars: map[string]string{
				"USER_AGENT": "",
			},
			wantContent: []string{
				"USER_AGENT=",
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Create .env.example file
			if err := os.WriteFile(filepath.Join(tmpDir, envExampleFile), []byte(tt.envExample), 0644); err != nil {
				t.Fatalf("Failed to create .env.example: %v", err)
			}

			// Run updateEnvFile
			if err := updateEnvFile(tt.envVars); err != nil {
				t.Fatalf("updateEnvFile() error = %v", err)
			}

			// Read resulting .env file
			content, err := os.ReadFile(filepath.Join(tmpDir, envFilename))
			if err != nil {
				t.Fatalf("Failed to read .env file: %v", err)
			}

			// Check each expected line exists in the file
			lines := strings.Split(strings.TrimSpace(string(content)), "\n")
			for _, want := range tt.wantContent {
				found := false
				for _, line := range lines {
					if line == want {
						found = true
						break
					}
				}
				if !found {
					t.Errorf("Expected line %q not found in .env file. Got content:\n%s", want, content)
				}
			}
		})
	}
}
