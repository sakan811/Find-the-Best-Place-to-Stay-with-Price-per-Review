package tests

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

// MockRequest contains only what we need for testing
type MockRequest struct {
	headers map[string]string
	url     string
}

func (m *MockRequest) Headers() map[string]string {
	return m.headers
}

func (m *MockRequest) URL() string {
	return m.url
}

func TestExtractXHeaders(t *testing.T) {
	// Create a temporary directory for testing
	tmpDir, err := os.MkdirTemp("", "test")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Set up test environment
	execDir = tmpDir

	// Create test .env.example file with the exact case we want
	exampleContent := "USER_AGENT=example\nX_BOOKING_CLIENT_TYPE=test\n"
	if err := os.WriteFile(filepath.Join(tmpDir, envExampleFile), []byte(exampleContent), 0644); err != nil {
		t.Fatalf("Failed to create .env.example: %v", err)
	}

	// Create mock request with test headers
	mockReq := &MockRequest{
		headers: map[string]string{
			"user-agent":            "Mozilla/5.0",
			"x-booking-client-type": "browser",
		},
		url: "https://www.booking.com/dml/graphql",
	}

	// Test header extraction
	if err := handleRequest(mockReq); err != nil {
		t.Fatalf("handleRequest() error = %v", err)
	}

	// Verify .env file was created and contains expected content
	content, err := os.ReadFile(filepath.Join(tmpDir, envFilename))
	if err != nil {
		t.Errorf("Failed to read created .env file: %v", err)
		return
	}

	// Check for expected content exactly
	expectedContent := "USER_AGENT=Mozilla/5.0\nX_BOOKING_CLIENT_TYPE=browser"
	if strings.TrimSpace(string(content)) != expectedContent {
		t.Errorf("Expected content:\n%s\n\nGot content:\n%s", expectedContent, string(content))
	}
}
