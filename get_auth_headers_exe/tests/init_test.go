package main

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

var (
	execDir        string
	envFilename    = ".env"
	envExampleFile = ".env.example"
	composeFile    = "docker-compose.yml"
)

func updateEnvFile(vars map[string]string) error {
	content := ""
	for k, v := range vars {
		content += k + "=" + v + "\n"
	}
	return os.WriteFile(filepath.Join(execDir, envFilename), []byte(content), 0644)
}

func writeEmbeddedFile(filename, content string) error {
	return os.WriteFile(filepath.Join(execDir, filename), []byte(content), 0644)
}

func checkFiles() error {
	// Create docker-compose.yml
	if err := writeEmbeddedFile(composeFile, "version: '3'\n"); err != nil {
		return err
	}

	// Create .env.example
	return writeEmbeddedFile(envExampleFile, "USER_AGENT=example\n")
}

func TestWriteEmbeddedFile(t *testing.T) {
	// Create a temporary directory for testing
	tmpDir, err := os.MkdirTemp("", "test")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Save original execDir and restore it after test
	originalExecDir := execDir
	execDir = tmpDir
	defer func() { execDir = originalExecDir }()

	tests := []struct {
		name     string
		filename string
		content  string
	}{
		{
			name:     "Write new file",
			filename: "test.txt",
			content:  "test content",
		},
		{
			name:     "Write existing file",
			filename: "existing.txt",
			content:  "existing content",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// For "existing file" test, create the file first
			if tt.name == "Write existing file" {
				fullPath := filepath.Join(tmpDir, tt.filename)
				if err := os.WriteFile(fullPath, []byte("original content"), 0644); err != nil {
					t.Fatalf("Failed to create existing file: %v", err)
				}
			}

			// Test writeEmbeddedFile
			err := writeEmbeddedFile(tt.filename, tt.content)
			if err != nil {
				t.Errorf("writeEmbeddedFile() error = %v", err)
				return
			}

			// Verify file exists
			fullPath := filepath.Join(tmpDir, tt.filename)
			if _, err := os.Stat(fullPath); os.IsNotExist(err) {
				t.Errorf("File was not created: %v", err)
				return
			}
		})
	}
}

func TestUpdateEnvFile(t *testing.T) {
	// Create a temporary directory for testing
	tmpDir, err := os.MkdirTemp("", "test")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Save original execDir and restore it after test
	originalExecDir := execDir
	execDir = tmpDir
	defer func() { execDir = originalExecDir }()

	// Create test .env.example file
	exampleContent := `USER_AGENT=example
X_BOOKING_CLIENT_TYPE=test
X_BOOKING_PAGE_ORIGIN=test`
	if err := os.WriteFile(filepath.Join(tmpDir, envExampleFile), []byte(exampleContent), 0644); err != nil {
		t.Fatalf("Failed to create test .env.example: %v", err)
	}

	// Test data
	envVars := map[string]string{
		"USER_AGENT":            "Mozilla/5.0",
		"X_BOOKING_CLIENT_TYPE": "browser",
		"X_BOOKING_PAGE_ORIGIN": "booking.com",
	}

	// Run updateEnvFile
	err = updateEnvFile(envVars)
	if err != nil {
		t.Errorf("updateEnvFile() error = %v", err)
		return
	}

	// Verify .env file was created and contains expected content
	content, err := os.ReadFile(filepath.Join(tmpDir, envFilename))
	if err != nil {
		t.Errorf("Failed to read created .env file: %v", err)
		return
	}

	// Check if all variables are present in the file
	for key, value := range envVars {
		expected := key + "=" + value
		if !contains(string(content), expected) {
			t.Errorf("Expected %s in .env file, but it was not found", expected)
		}
	}
}

func TestCheckFiles(t *testing.T) {
	// Create a temporary directory for testing
	tmpDir, err := os.MkdirTemp("", "test")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Save original execDir and restore it after test
	originalExecDir := execDir
	execDir = tmpDir
	defer func() { execDir = originalExecDir }()

	// Run checkFiles
	err = checkFiles()
	if err != nil {
		t.Errorf("checkFiles() error = %v", err)
		return
	}

	// Verify both files were created
	files := []string{composeFile, envExampleFile}
	for _, file := range files {
		if _, err := os.Stat(filepath.Join(tmpDir, file)); os.IsNotExist(err) {
			t.Errorf("File %s was not created", file)
		}
	}
}

// Helper function to check if a string contains another string
func contains(s, substr string) bool {
	return strings.Contains(s, substr)
}
