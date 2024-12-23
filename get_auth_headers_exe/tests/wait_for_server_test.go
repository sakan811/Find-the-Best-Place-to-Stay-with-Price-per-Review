package tests

import (
	"fmt"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

func TestWaitForServer(t *testing.T) {
	tests := []struct {
		name        string
		serverDelay time.Duration
		expectError bool
	}{
		{
			name:        "Server starts immediately",
			serverDelay: 0,
			expectError: false,
		},
		{
			name:        "Server starts after delay",
			serverDelay: 2 * time.Second,
			expectError: false,
		},
		{
			name:        "Server never starts",
			serverDelay: 31 * time.Second,
			expectError: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Create test server
			server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				time.Sleep(tt.serverDelay)
				fmt.Fprintln(w, "ok")
			}))
			defer server.Close()

			// Override http.Get to use our test server
			originalGet := httpGet
			httpGet = func(url string) (*http.Response, error) {
				if tt.serverDelay >= 31*time.Second {
					return nil, fmt.Errorf("connection refused")
				}
				return originalGet(server.URL)
			}
			defer func() { httpGet = originalGet }()

			// Run the test
			err := waitForServer()

			// Check error expectations
			if tt.expectError {
				if err == nil {
					t.Error("Expected an error but got none")
				}
			} else {
				if err != nil {
					t.Errorf("Unexpected error: %v", err)
				}
			}
		})
	}
}
