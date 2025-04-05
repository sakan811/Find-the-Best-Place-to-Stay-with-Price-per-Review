# Finding the Best Place to Stay with Price per Review from Booking.com

**Discover** the **ideal accommodation** with a **Price/Review** analyzer for Booking.com using **web-scraping** technology through an intuitive **web-app**.

This application helps you identify the best value accommodations in your desired destination by calculating a **Price/Review Score** for each property available during your specified travel dates.

A **lower Price/Review Score** represents exceptional value—a property that offers **high-quality experiences** (as reflected in its reviews) at a **reasonable price point**.

## Status

[![Backend Test](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/backend-test.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/backend-test.yml)

[![Frontend Test](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/frontend-test.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/frontend-test.yml)

[![Docker Build](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/docker-build.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/docker-build.yml)

[![Push to Docker Hub](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/docker-push.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/docker-push.yml)

## How to Use the Web App

### Step 0: Prerequisites

- **Docker Desktop** must be installed on your system for containerization.

### Step 1: Set Up the Web App

1. Install Docker Desktop
   - [Download Docker Desktop here](https://www.docker.com/products/docker-desktop) and follow the installation instructions for your operating system.

2. Obtain the [Docker Compose](./docker-compose.yml) file from this repository.

3. Save the file to a directory of your choice on your local machine.

4. Create an empty `.env` file in the same directory:
   - This file will store necessary authentication variables.
   - In a terminal, navigate to your directory and run `touch ./.env` (Git Bash) or create it manually.

### Step 2: Access the Web App

1. Ensure Docker Desktop is running on your system.
   - Launch Docker Desktop if it's not already running.

2. Obtain your browser's User-Agent:
   - Visit <https://www.whatismybrowser.com/detect/what-is-my-user-agent/>
   - Copy the displayed **User-Agent** string.
   - Edit the `docker-compose.yml` file and replace the value after `- USER_AGENT=` with your copied string.

3. Run the Auth Headers App:

   3.1 Deploy the **Auth Headers App** container:

      ```bash
      docker-compose --profile phase1 up -d
      ```

   3.2 Generate and save authentication headers:

      ```bash
      curl -s "http://localhost:4000/extract-headers?save=true"
      ```

      - This process extracts necessary authentication headers from Booking.com and saves them to your `.env` file.

4. Launch the Main Application:

   4.1 Deploy the **Web App** container:

      ```bash
      docker-compose --profile phase2 up -d
      ```

      - This command starts all necessary services in the background.
      - Access the application through your browser at <http://localhost:5000>.

## Disclaimer

- When specifying currency in the form, use standard three-letter abbreviations:
  - Example: For US Dollars, enter **USD** in the currency field.

- The "Scrape Hotel Properties Only" option affects search results:
  - When checked: Only traditional hotels will be included in results.
  - When unchecked: All accommodation types (apartments, guest houses, etc.) will be included.

- Country names must be entered in full:
  - Correct: "United Kingdom" or "Thailand"
  - Incorrect: "UK" or "TH"
