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

### Step 2: Find Your User Agent
1. **Find Your User Agent**
   - Open your web browser and go to [What Is My Browser](https://www.whatismybrowser.com/detect/what-is-my-user-agent/).
   - You will see a message that shows your User Agent. 
   - Copy the User Agent.

2. **Edit `.env` file**
   - Rename the `.env.example` file to `.env`.
   - Open the `.env` via a text editor like Notepad, etc.
   - Look for the line that says `USER_AGENT`.
   - Paste the User Agent you copied, for exaxmple:
     ```
     USER_AGENT=copied_user_agent
     ```
     - Where `copied_user_agent` is the User Agent you copied.
   - Save the file and close the text editor.
  
### Step 3: Find Necessary Headers

1. **Open Booking.com**
   - Go to [Booking.com](https://www.booking.com).
   - Search for any destination (like "Tokyo" or "New York") to see a list of available places.

2. **Open Developer Tools:**
   - Make sure you are on the page showing the available places for booking.
   - Scroll down a bit on the page.
   - Open the Developer Tools (a set of tools to inspect web pages):
     - **For Chrome:**
       - Right-click anywhere on the page.
       - Click on `Inspect`.
       - Click on the `Network` tab at the top of the Developer Tools.
     - **For Firefox:**
       - Right-click anywhere on the page.
       - Click on `Inspect`.
       - Click on the `Network` tab at the top.

3. **Find GraphQL Request:**
   - In the **filter** bar at the top of the Network tab, type `graphql`.
     
   > If you don't see any requests start with `graphql` or named `graphql` right away, scroll down the Booking.com page a little more. 
   > This will load more requests in the Network tab, and you may find the `graphql` request there.

4. **Inspect a Request:**
   - Click on the request start with `graphql` or named `graphql` from the list in the Network tab.
   - Look for the section labeled **Headers**. This section contains details about what was sent to the server.

5. **Find the Necessary Headers:**
   - Look for these specific headers in the Headers section:
     - `X-BOOKING-CONTEXT-ACTION-NAME`
     - `X-BOOKING-CONTEXT-AID`
     - `X-BOOKING-CSRF-TOKEN`
     - `X-BOOKING-ET-SERIALIZED-STATE`
     - `X-BOOKING-PAGEVIEW-ID`
     - `X-BOOKING-SITE-TYPE-ID`
     - `X-BOOKING-TOPIC`

6. **Copy Header Values:**
   - For each header, right-click on it and select `Copy Value`. This copies the information to your clipboard.

7. **Save the Values Locally:**
   - Open a text editor and create a new file named `.env`.
   - Paste each copied value into the file next to its corresponding name, like this:
     ```
     X_BOOKING_CONTEXT_ACTION_NAME=copied_action_name
     X_BOOKING_CONTEXT_AID=copied_aid
     X_BOOKING_CSRF_TOKEN=copied_csrf_token
     X_BOOKING_ET_SERIALIZED_STATE=copied_serialized_state
     X_BOOKING_PAGEVIEW_ID=copied_pageview_id
     X_BOOKING_SITE_TYPE_ID=copied_site_type_id
     X_BOOKING_TOPIC=copied_topic
     ```

### Step 4: Access the Web App
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
