package main

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/playwright-community/playwright-go"
)

var intercepted bool

const envFilename = ".env"

func main() {
	err := playwright.Install()
	if err != nil {
		log.Fatalf("Could not install playwright: %v", err)
	}

	err = extractXHeaders()
	if err != nil {
		log.Fatal(err)
	}
}

func extractXHeaders() error {
	pw, err := playwright.Run()
	if err != nil {
		return fmt.Errorf("could not start playwright: %v", err)
	}
	browser, err := pw.Chromium.Launch(playwright.BrowserTypeLaunchOptions{
		Headless: playwright.Bool(false),
	})
	if err != nil {
		return fmt.Errorf("could not launch browser: %v", err)
	}
	page, err := browser.NewPage()
	if err != nil {
		return fmt.Errorf("could not create page: %v", err)
	}

	page.On("request", handleRequest)

	if _, err = page.Goto("https://www.booking.com"); err != nil {
		return fmt.Errorf("could not goto: %v", err)
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

	if err = browser.Close(); err != nil {
		return fmt.Errorf("could not close browser: %v", err)
	}
	if err = pw.Stop(); err != nil {
		return fmt.Errorf("could not stop Playwright: %v", err)
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

			updateEnvExample(envVars)
			intercepted = true
		}
	}
}

func updateEnvExample(envVars map[string]string) {
	envExamplePath := filepath.Join(".", ".env.example")
	envPath := filepath.Join(".", envFilename)

	content, err := os.ReadFile(envExamplePath)
	if err != nil {
		log.Printf("Error reading .env.example: %v", err)
		return
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
		log.Printf("Error writing to %s: %v", envFilename, err)
		return
	}

	fmt.Printf("Headers updated in %s file\n", envFilename)
}
