# Finding the Best Place to Stay with Price per Review from Booking.com using Web-Scraping

**Finding** the **best place** to stay with **Price/Review** from Booking.com using **web-scraping** via a local **web-app**.

Aim to provide **Price/Review Score** of the places located in the specified city,
when finding a place to stay in that city during a trip.  

A **lower Price/Review Score** indicates that the place is **not expensive**, yet, with a **great review score**.

## Status

[![Backend Test](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/backend-test.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/backend-test.yml)

[![Frontend Test](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/frontend-test.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/frontend-test.yml)

[![Docker Build](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/docker-build.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/docker-build.yml)

[![Push to Docker Hub](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/docker-push.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/docker-push.yml)

## How to Use the Web App

### Step 0: Prerequisites

- **Docker Desktop** must be installed on your computer.
- **Make** must be installed on your computer.

### Step 1: Set Up the Web App

1. Install Docker Desktop
   - [Click here](https://www.docker.com/products/docker-desktop) to download **Docker Desktop**.
   - Follow the instructions on the website to install it on your computer.
2. Download [Docker Compose](./docker-compose.yml) file from this repository.
3. Place the file in any directory of your choice.
4. Create an empty `.env` file in the same directory as the `docker-compose.yml` file.
   - This file will be used to store environment variables.
   - run `touch ./.env` in Git Bash terminal to create the file.

### Step 2: Access the Web App

1. Make sure that the Docker Desktop is running.
   - If not, start the Docker Desktop.

2. Navigate to <https://www.whatismybrowser.com/detect/what-is-my-user-agent/>
   - Copy the **User-Agent** string from the website.
   - Paste the **User-Agent** string into the `docker-compose.yml` file.
   - Find the line that starts with `- USER_AGENT=` and replace the value with your copied **User-Agent** string.

3. Run Auth Headers App:

   3.1 Pull the latest version of the **Auth Headers App** from Docker Hub:

      ```bash
      make docker-compose-auth-headers
      ```

   3.2 Run the **Auth Headers App**:

      ```bash
      make extract-headers-with-save
      ```

      - This command will run the **Auth Headers App** in detached mode and save the headers to the `.env` file.

4. Run the Web App:

   4.1 Pull the latest version of the **Web App** from Docker Hub:

      ```bash
      make docker-compose-app
      ```

      - This command will run the **Web App** in detached mode.
      - The **Web App** will be accessible at <http://localhost:5000>.

## Disclaimer

- When filling out the form, please use abbreviations for **currency**:
  - For example, if you want to select the US Dollar, enter **USD** in the currency tab.

- If you tick the **Scrape Hotel Properties Only** box, the scraper will only gather data on hotels.
  - If you leave this box unticked, the scraper will retrieve information on all types of places available through Booking.com in the specified city.

- When entering the **country** in the form, please provide the **full name** of the country.
  - **Do not** use abbreviations.
