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
	"os/signal"
	"syscall"
	"net/http"
	"time"

	"github.com/playwright-community/playwright-go"
)

var intercepted bool

const (
	envFilename    = ".env"
	envExampleFile = ".env.example"
	composeFile    = "docker-compose.yml"
)

func main() {
	log.Println("Starting application...")

	if err := checkFiles(); err != nil {
		log.Fatalf("File check failed: %v", err)
	}

	if err := playwright.Install(); err != nil {
		log.Fatalf("Could not install Playwright: %v", err)
	}

	if err := extractXHeaders(); err != nil {
		log.Fatalf("Header interception failed: %v", err)
	}

	if err := runDockerCompose(); err != nil {
		log.Fatalf("Docker Compose failed: %v", err)
	}

	gracefulShutdown()

	if err := waitForServer(); err != nil {
		log.Fatalf("Server did not start: %v", err)
	}

	if err := openBrowser("http://localhost:5000"); err != nil {
		log.Printf("Failed to open browser: %v", err)
	}

	select {}
}

func checkFiles() error {
	files := []string{envExampleFile, composeFile}
	for _, file := range files {
		if _, err := os.Stat(file); os.IsNotExist(err) {
			return fmt.Errorf("required file %s not found", file)
		}
	}
	return nil
}

func extractXHeaders() error {
	log.Println("Starting header interception with Playwright...")
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

	log.Println("Header interception successful")
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

			if err := updateEnvFile(envVars); err != nil {
				log.Printf("Failed to update env file: %v", err)
			}
			intercepted = true
		}
	}
}

func updateEnvFile(envVars map[string]string) error {
	envExamplePath := filepath.Join(".", envExampleFile)
	envPath := filepath.Join(".", envFilename)

	content, err := os.ReadFile(envExamplePath)
	if err != nil {
		return fmt.Errorf("error reading %s: %v", envExampleFile, err)
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

	if err := os.WriteFile(envPath, []byte(strings.Join(updatedLines, "\n")), 0644); err != nil {
		return fmt.Errorf("error writing to %s: %v", envFilename, err)
	}

	log.Printf("Headers updated in %s file", envFilename)
	return nil
}

func runDockerCompose() error {
	log.Println("Starting Docker Compose...")
	if _, err := os.Stat(composeFile); os.IsNotExist(err) {
		return fmt.Errorf("docker-compose.yml file not found")
	}

	cmd := exec.Command("docker-compose", "up", "-d")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	return cmd.Run()
}

func gracefulShutdown() {
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	go func() {
		<-c
		log.Println("Shutting down...")
		cmd := exec.Command("docker-compose", "down")
		cmd.Stdout = os.Stdout
		cmd.Stderr = os.Stderr
		if err := cmd.Run(); err != nil {
			log.Printf("Error during shutdown: %v", err)
		}
		os.Exit(0)
	}()
}

func waitForServer() error {
	log.Println("Waiting for server to start...")
	for i := 0; i < 30; i++ {
		resp, err := http.Get("http://localhost:5000")
		if err == nil {
			resp.Body.Close()
			log.Println("Server is up and running")
			return nil
		}
		time.Sleep(time.Second)
	}
	return fmt.Errorf("server did not start within the expected time")
}

func openBrowser(url string) error {
	log.Printf("Attempting to open browser at %s", url)
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