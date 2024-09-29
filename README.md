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

## How to Use the Web App

### Step 1: Set Up the Web App
1. **Install Docker Desktop**
   - [Click here](https://www.docker.com/products/docker-desktop) to download Docker Desktop.
   - Follow the instructions on the website to install it on your computer.
2. Download Web App Assets
   - Click here to [Click here](https://www.docker.com/products/docker-desktop) to download the web-app assets.
   - Extract the ZIP file.

### Step 2: Find Your User Agent
1. **Find Your User Agent**
   - Open your web browser and go to [What Is My Browser](https://www.whatismybrowser.com/detect/what-is-my-user-agent/).
   - You will see a message that shows your User Agent. **Copy this text.**

2. **Edit the Configuration File**
   - Open the `docker-compose.yml` file you extracted from the ZIP file in a text editor (like Notepad).
   - Look for the line that says `USER_AGENT`. Replace `your_user_agent` text with the User Agent you copied. 
   - Save the file and close the text editor.

### Step 3: Access the Web App
1. **Start the Web App**
   - Make sure that the Docker Desktop is running.
      - If not, start the Docker Desktop. 
   - Double-click the executable file:
     - **Windows:** Double-click `app-windows.exe`
     - **macOS:** Double-click `app-mac.exe`
     - **Linux:** Double-click `app-linux.exe`
2. **Check the Terminal**:
     - A terminal window will open, indicating that the web app is starting. 
       You should see messages in the terminal that confirm the app is launching.

3. **Access the Web App**
   - Open your web browser and go to: [http://localhost:5000/](http://localhost:5000/)

### Step 4: Exit the Web App
- Press `Enter` as prompted in the terminal.
  - Alternatively, you can open Docker Desktop and stop the container from the **Containers** section.

## Disclaimer

- When filling out the form, please use abbreviations for **currency**:
  - For example, if you want to select the US Dollar, enter **USD** in the currency tab.

- If you tick the **Scrape Hotel Properties Only** box, the scraper will only gather data on hotels. 
  - If you leave this box unticked, the scraper will retrieve information on all types of places available through Booking.com in the specified city.

- When entering the **country** in the form, please provide the **full name** of the country. 
  - **Do not** use abbreviations.