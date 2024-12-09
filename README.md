# Finding the Best Place to Stay with Price per Review from Booking.com using Web-Scraping
**Finding** the **best place** to stay with **Price/Review** from Booking.com using **web-scraping** via a local **web-app**.

Aim to provide **Price/Review Score** of the places located in the specified city,
when finding a place to stay in that city during a trip.  

A **lower Price/Review Score** indicates that the place is **not expensive**, yet, with a **great review score**.   

## Status
[![CodeQL](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/codeql.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/codeql.yml)  

[![Backend Test](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/backend-test.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/backend-test.yml)

[![Frontend Test](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/frontend-test.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/frontend-test.yml)

[![Docker Build](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/docker-build.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/docker-build.yml)

[![Trivy Docker Scan](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/trivy-scan.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/trivy-scan.yml)

## How to Use the Web App

### Step 1: Set Up the Web App
1. Install Docker Desktop
   - [Click here](https://www.docker.com/products/docker-desktop) to download **Docker Desktop**.
   - Follow the instructions on the website to install it on your computer.
2. Download Docker Compose File
   - Download the [docker-compose.yml](docker-compose.yml) file from this repository.
   - Place the file in the directory of your choice.
3. Download `.env.example` File
   - Download the [.env.example](.env.example) file from this repository.
   - Place the file in the same directory with Docker Compose file.

### Step 2: Setup the Necessary Headers
1. Download the executable file inside [get_auth_headers_exe](get_auth_headers_exe) folder depend on your OS.
2. Place the file in the same directory as `.env.example` and `docker-compose.yml` files.
3. Run the executable file.

### Step 3: Access the Web App
1. **Start the Web App**
   - Make sure that the Docker Desktop is running.
      - If not, start the Docker Desktop. 
   - Open the terminal
   - Use the `cd` command to go to the folder where you saved the `docker-compose.yml` file.  
     Example:
     ```bash
     cd /path/to/directory
     ```
   - Run `docker-compose up` to start the web app.

2. **Access the Web App**
   - Open your web browser and go to: [http://localhost:5000/](http://localhost:5000/)

### Step 5: Stop the Web App
1. **Open Docker Desktop**  
   - Go to the **Containers** section.  

2. **Stop the Container**  
   - Find the running container for the web app and click **Stop**.

## Disclaimer

- When filling out the form, please use abbreviations for **currency**:
  - For example, if you want to select the US Dollar, enter **USD** in the currency tab.

- If you tick the **Scrape Hotel Properties Only** box, the scraper will only gather data on hotels. 
  - If you leave this box unticked, the scraper will retrieve information on all types of places available through Booking.com in the specified city.

- When entering the **country** in the form, please provide the **full name** of the country. 
  - **Do not** use abbreviations.
