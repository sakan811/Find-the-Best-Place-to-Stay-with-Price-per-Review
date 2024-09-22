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

2. **Download the Configuration File**
   - [Click here](docker-compose.yml) to download the docker-compose.yml file.
   - Save it in a folder where you can easily find it (e.g., your Desktop or Documents).

3. **Find Your User Agent**
   - Open your web browser and go to [What Is My Browser](https://www.whatismybrowser.com/detect/what-is-my-user-agent/).
   - You will see a message that shows your User Agent. **Copy this text.**

4. **Edit the Configuration File**
   - Open the `docker-compose.yml` file you downloaded in a text editor (like Notepad).
   - Look for the line that says `USER_AGENT`. Replace `your_user_agent` text with the User Agent you copied. 
   - Save the file and close the text editor.

5. **Start the Web App**
   - Make sure that the Docker Desktop is running.
      - If not, start the Docker Desktop. 
   - Open a **Command Prompt**, **Terminal**, or **Console** window on your computer:
     - **Windows:** Search for "Command Prompt" or "cmd" in the Start menu.
     - **macOS:** Open "Terminal" from the Applications > Utilities folder, or search for it using Spotlight (Cmd + Space).
     - **Linux:** Open "Terminal" from your applications menu or use the shortcut Ctrl + Alt + T.
   - Navigate to the folder where you saved the `docker-compose.yml` file. You can do this by typing `cd path_to_your_folder`, where `path_to_your_folder` is the location of your file. 
   - Type the following command and press **Enter**:
     ```
     docker-compose up
     ```

### Step 2: Access the Web App
- Open your web browser and go to: [http://localhost:5000/](http://localhost:5000/)
- To stop the web app, return to the Command Prompt or Terminal window and press **Ctrl + C**. 
  - Alternatively, you can open Docker Desktop and stop the container from the **Containers** section.

## Disclaimer

- When filling out the form, please use abbreviations for **currency**:
  - For example, if you want to select the US Dollar, enter **USD** in the currency tab.

- If you tick the **Scrape Hotel Properties Only** box, the scraper will only gather data on hotels. 
  - If you leave this box unticked, the scraper will retrieve information on all types of places available through Booking.com in the specified city.

- When entering the **country** in the form, please provide the **full name** of the country. 
  - **Do not** use abbreviations.