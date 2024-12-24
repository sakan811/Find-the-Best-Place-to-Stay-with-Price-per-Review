package tests

import (
	"os"
	"path/filepath"
	"testing"
)

func TestWriteEmbeddedFileContent(t *testing.T) {
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
			content:  "new content",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if tt.name == "Write existing file" {
				// Create the file first
				path := filepath.Join(tmpDir, tt.filename)
				if err := os.WriteFile(path, []byte("original content"), 0644); err != nil {
					t.Fatalf("Failed to create existing file: %v", err)
				}
			}

			err := writeEmbeddedFile(tt.filename, tt.content)
			if err != nil {
				t.Errorf("writeEmbeddedFile() error = %v", err)
				return
			}

			// Verify content
			content, err := os.ReadFile(filepath.Join(tmpDir, tt.filename))
			if err != nil {
				t.Errorf("Failed to read file: %v", err)
				return
			}
			if string(content) != tt.content {
				t.Errorf("Expected content %q, got %q", tt.content, string(content))
			}
		})
	}
}
