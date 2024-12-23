package tests

import (
	"fmt"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"runtime"
	"strings"
	"testing"
	"time"
)

var (
	execDir        string
	envFilename    = ".env"
	envExampleFile = ".env.example"
	composeFile    = "docker-compose.yml"
	intercepted    bool
	httpGet        = http.Get
	goos           = runtime.GOOS
)

func updateEnvFile(vars map[string]string) error {
	// Read existing content from .env.example
	examplePath := filepath.Join(execDir, envExampleFile)
	content, err := os.ReadFile(examplePath)
	if err != nil {
		return fmt.Errorf("error reading %s: %v", envExampleFile, err)
	}

	lines := strings.Split(string(content), "\n")
	updatedLines := make([]string, 0, len(lines))

	for _, line := range lines {
		if parts := strings.SplitN(line, "=", 2); len(parts) == 2 {
			key := strings.TrimSpace(parts[0])
			if value, exists := vars[key]; exists {
				line = fmt.Sprintf("%s=%s", key, value)
			}
		}
		if line != "" {
			updatedLines = append(updatedLines, line)
		}
	}

	return os.WriteFile(filepath.Join(execDir, envFilename), []byte(strings.Join(updatedLines, "\n")), 0644)
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

func handleRequest(request *MockRequest) error {
	if matched, _ := regexp.MatchString(`https://www\.booking\.com/dml/graphql.*`, request.URL()); matched {
		headers := request.Headers()
		envVars := make(map[string]string)

		// Create a map of existing env vars from .env.example
		examplePath := filepath.Join(execDir, envExampleFile)
		content, err := os.ReadFile(examplePath)
		if err != nil {
			return fmt.Errorf("error reading %s: %v", envExampleFile, err)
		}

		envKeys := make(map[string]string) // lowercase -> actual case
		for _, line := range strings.Split(string(content), "\n") {
			if parts := strings.SplitN(line, "=", 2); len(parts) == 2 {
				key := strings.TrimSpace(parts[0])
				envKeys[strings.ToLower(key)] = key
			}
		}

		// Match headers to env vars case-insensitively
		for key, value := range headers {
			if strings.HasPrefix(key, "x-") || key == "user-agent" {
				envKey := strings.ToUpper(strings.ReplaceAll(key, "-", "_"))
				if actualKey, exists := envKeys[strings.ToLower(envKey)]; exists {
					envVars[actualKey] = value
				}
			}
		}

		intercepted = true
		return updateEnvFile(envVars)
	}
	return nil
}

func runDockerCompose() error {
	composePath := filepath.Join(execDir, composeFile)
	if _, err := os.Stat(composePath); os.IsNotExist(err) {
		return fmt.Errorf("docker-compose.yml file not found")
	}

	cmd := execCommand("docker-compose", "-f", composePath, "up", "-d")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	return cmd.Run()
}

func gracefulShutdown() {
	composePath := filepath.Join(execDir, composeFile)
	cmd := execCommand("docker-compose", "-f", composePath, "down")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	if err := cmd.Run(); err != nil {
		fmt.Printf("Error during shutdown: %v\n", err)
	}
}

func waitForServer() error {
	for i := 0; i < 30; i++ {
		resp, err := httpGet("http://localhost:5000")
		if err == nil {
			resp.Body.Close()
			return nil
		}
		time.Sleep(time.Second)
	}
	return fmt.Errorf("server did not start within the expected time")
}

func openBrowser(url string) error {
	var cmd *exec.Cmd

	switch goos {
	case "linux":
		cmd = execCommand("xdg-open", url)
	case "windows":
		cmd = execCommand("rundll32", "url.dll,FileProtocolHandler", url)
	case "darwin":
		cmd = execCommand("open", url)
	default:
		return fmt.Errorf("unsupported platform")
	}

	return cmd.Start()
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

func TestUpdateEnvFileInit(t *testing.T) {
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

func TestCheckFilesCreation(t *testing.T) {
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
