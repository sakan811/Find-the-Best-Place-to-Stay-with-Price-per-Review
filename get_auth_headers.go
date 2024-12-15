package main

import (
	"fmt"
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"runtime"
	"strings"

	"github.com/playwright-community/playwright-go"
)

var intercepted bool

const (
	envFilename    = ".env"
	envExampleFile = ".env.example"
	composeFile    = "docker-compose.yml"
)

func main() {
	err := playwright.Install()
	if err != nil {
		log.Fatalf("Could not install Playwright: %v", err)
	}

	fmt.Println("Starting header interception with Playwright...")
	err = extractXHeaders()
	if err != nil {
		log.Fatalf("Header interception failed: %v", err)
	}

	fmt.Println("Header interception successful! Starting Docker Compose...")
	err = runDockerCompose()
	if err != nil {
		log.Fatalf("Docker Compose failed: %v", err)
	}

	fmt.Println("Navigating to http://localhost:5000")
	err = openBrowser("http://localhost:5000")
	if err != nil {
		log.Printf("Failed to open browser: %v", err)
	}
}

func extractXHeaders() error {
	pw, err := playwright.Run()
	if err != nil {
		return fmt.Errorf("could not start Playwright: %v", err)
	}
	defer pw.Stop()

	browser, err := pw.Chromium.Launch(playwright.BrowserTypeLaunchOptions{
		Headless: playwright.Bool(false),
	})
	if err != nil {
		return fmt.Errorf("could not launch browser: %v", err)
	}
	defer browser.Close()

	page, err := browser.NewPage()
	if err != nil {
		return fmt.Errorf("could not create page: %v", err)
	}

	page.On("request", handleRequest)

	if _, err = page.Goto("https://www.booking.com"); err != nil {
		return fmt.Errorf("could not navigate to the URL: %v", err)
	}

	if err = page.Fill("input[name=\"ss\"]", "Tokyo"); err != nil {
		return fmt.Errorf("could not fill input: %v", err)
	}
	if err = page.Press("input[name=\"ss\"]", "Enter"); err != nil {
		return fmt.Errorf("could not press Enter: %v", err)
	}

	if err = page.WaitForLoadState(playwright.PageWaitForLoadStateOptions{
		State: playwright.LoadStateNetworkidle,
	}); err != nil {
		return fmt.Errorf("could not wait for network idle: %v", err)
	}

	if !intercepted {
		return fmt.Errorf("no matching headers intercepted")
	}

	return nil
}

func handleRequest(request playwright.Request) {
	if !intercepted {
		matched, _ := regexp.MatchString(`https://www\.booking\.com/dml/graphql.*`, request.URL())
		if matched {
			headers := request.Headers()
			envVars := make(map[string]string)

			for key, value := range headers {
				if strings.HasPrefix(key, "x-") || key == "user-agent" {
					envKey := strings.ToUpper(strings.ReplaceAll(key, "-", "_"))
					envVars[envKey] = value
				}
			}

			updateEnvFile(envVars)
			intercepted = true
		}
	}
}

func updateEnvFile(envVars map[string]string) {
	envExamplePath := filepath.Join(".", envExampleFile)
	envPath := filepath.Join(".", envFilename)

	content, err := os.ReadFile(envExamplePath)
	if err != nil {
		log.Fatalf("Error reading %s: %v", envExampleFile, err)
	}

	lines := strings.Split(string(content), "\n")
	updatedLines := make([]string, 0, len(lines))

	for _, line := range lines {
		parts := strings.SplitN(line, "=", 2)
		if len(parts) == 2 {
			key := strings.TrimSpace(parts[0])
			if value, exists := envVars[key]; exists {
				line = fmt.Sprintf("%s=%s", key, value)
			}
		}
		updatedLines = append(updatedLines, line)
	}

	err = os.WriteFile(envPath, []byte(strings.Join(updatedLines, "\n")), 0644)
	if err != nil {
		log.Fatalf("Error writing to %s: %v", envFilename, err)
	}

	fmt.Printf("Headers updated in %s file\n", envFilename)
}

func runDockerCompose() error {
	// Check if the compose file exists
	if _, err := os.Stat(composeFile); os.IsNotExist(err) {
		return fmt.Errorf("docker-compose.yml file not found")
	}

	// Execute `docker-compose up` in interactive mode
	cmd := exec.Command("docker-compose", "up")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	err := cmd.Run()
	if err != nil {
		return fmt.Errorf("docker-compose up failed: %v", err)
	}

	return nil
}

func openBrowser(url string) error {
	var cmd *exec.Cmd

	switch runtime.GOOS {
	case "linux":
		cmd = exec.Command("xdg-open", url)
	case "windows":
		cmd = exec.Command("rundll32", "url.dll,FileProtocolHandler", url)
	case "darwin":
		cmd = exec.Command("open", url)
	default:
		return fmt.Errorf("unsupported platform")
	}

	return cmd.Start()
}