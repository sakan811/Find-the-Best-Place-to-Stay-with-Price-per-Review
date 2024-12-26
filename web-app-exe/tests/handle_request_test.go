package tests

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestHandleRequest(t *testing.T) {
	// Create a temporary directory for testing
	tmpDir, err := os.MkdirTemp("", "test")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Set up test environment
	execDir = tmpDir

	// Create .env.example file
	envExample := "USER_AGENT=example\nX_BOOKING_CLIENT_TYPE=test\n"
	if err := os.WriteFile(filepath.Join(tmpDir, envExampleFile), []byte(envExample), 0644); err != nil {
		t.Fatalf("Failed to create .env.example: %v", err)
	}

	tests := []struct {
		name            string
		request         MockRequest
		expectIntercept bool
		expectHeaders   map[string]string
	}{
		{
			name: "matching URL with headers",
			request: MockRequest{
				url: "https://www.booking.com/dml/graphql",
				headers: map[string]string{
					"user-agent":            "Mozilla/5.0",
					"x-booking-client-type": "browser",
				},
			},
			expectIntercept: true,
			expectHeaders: map[string]string{
				"USER_AGENT":            "Mozilla/5.0",
				"X_BOOKING_CLIENT_TYPE": "browser",
			},
		},
		{
			name: "non-matching URL",
			request: MockRequest{
				url: "https://www.booking.com/other",
				headers: map[string]string{
					"user-agent": "Mozilla/5.0",
				},
			},
			expectIntercept: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Reset intercepted flag
			intercepted = false

			// Remove any existing .env file
			os.Remove(filepath.Join(tmpDir, envFilename))

			// Run handleRequest
			handleRequest(&tt.request)

			// Check if interception occurred as expected
			if intercepted != tt.expectIntercept {
				t.Errorf("Expected intercepted to be %v, got %v", tt.expectIntercept, intercepted)
			}

			if tt.expectIntercept {
				// Verify .env file contents
				envContent, err := os.ReadFile(filepath.Join(tmpDir, envFilename))
				if err != nil {
					t.Fatalf("Failed to read .env file: %v", err)
				}

				// Check for expected headers
				for key, value := range tt.expectHeaders {
					expected := key + "=" + value
					if !strings.Contains(string(envContent), expected) {
						t.Errorf("Expected %s in .env file, got: %s", expected, string(envContent))
					}
				}
			}
		})
	}
}
