package tests

import (
	"os"
	"path/filepath"
	"testing"
	// Replace with your actual module path
)

// Add these variables
var (
	dockerComposeTemplate = "version: '3'\n"
	envExampleTemplate    = "USER_AGENT=example\n"
)

func TestCheckFiles(t *testing.T) {
	// Create a temporary directory for testing
	tmpDir, err := os.MkdirTemp("", "test-*")
	if err != nil {
		t.Fatalf("Failed to create temp directory: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Temporarily override execDir for testing
	originalExecDir := execDir
	execDir = tmpDir
	defer func() { execDir = originalExecDir }()

	// Test the checkFiles function
	err = checkFiles()
	if err != nil {
		t.Errorf("checkFiles() returned error: %v", err)
	}

	// Verify that files were created
	files := []string{composeFile, envExampleFile}
	for _, file := range files {
		path := filepath.Join(tmpDir, file)
		if _, err := os.Stat(path); os.IsNotExist(err) {
			t.Errorf("Expected file %s was not created", file)
		}
	}

	// Verify file contents
	composeContent, err := os.ReadFile(filepath.Join(tmpDir, composeFile))
	if err != nil {
		t.Errorf("Failed to read docker-compose.yml: %v", err)
	}
	if string(composeContent) != dockerComposeTemplate {
		t.Error("docker-compose.yml content does not match template")
	}

	envContent, err := os.ReadFile(filepath.Join(tmpDir, envExampleFile))
	if err != nil {
		t.Errorf("Failed to read .env.example: %v", err)
	}
	if string(envContent) != envExampleTemplate {
		t.Error(".env.example content does not match template")
	}
}

func TestCheckFilesExistingFiles(t *testing.T) {
	// Create a temporary directory for testing
	tmpDir, err := os.MkdirTemp("", "test-*")
	if err != nil {
		t.Fatalf("Failed to create temp directory: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Temporarily override execDir for testing
	originalExecDir := execDir
	execDir = tmpDir
	defer func() { execDir = originalExecDir }()

	// Create files before running checkFiles
	files := map[string]string{
		composeFile:    dockerComposeTemplate,
		envExampleFile: envExampleTemplate,
	}

	for file, content := range files {
		path := filepath.Join(tmpDir, file)
		if err := os.WriteFile(path, []byte(content), 0644); err != nil {
			t.Fatalf("Failed to create test file %s: %v", file, err)
		}
	}

	// Test the checkFiles function
	err = checkFiles()
	if err != nil {
		t.Errorf("checkFiles() returned error: %v", err)
	}

	// Verify files have correct content
	for file, expectedContent := range files {
		path := filepath.Join(tmpDir, file)
		content, err := os.ReadFile(path)
		if err != nil {
			t.Errorf("Failed to read %s: %v", file, err)
			continue
		}
		if string(content) != expectedContent {
			t.Errorf("File %s has unexpected content", file)
		}
	}
}
