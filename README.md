# Finding-the-Best-Place-to-Stay-with-Price-per-Review-from-Booking.com-using-Web-Scraping
Finding the Best Place to Stay with Price per Review from Booking.com using Web Scraping.  

Aim to provide places with Price/Review Score when finding a place to stay during a trip.  

A lower Price/Review Score indicates that the place isn't expensive, yet, with a great review score.   

## Status
Latest Update: 11 July 2024

[![CodeQL](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/codeql.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/codeql.yml)  

[![Python application](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/python-app.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/python-app.yml)

## To scrape data from Booking.com
- Install Node.js: https://nodejs.org/en
- Clone this repo: ```https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review.git```
- Run ```cd backend``` in the terminal
- Install all Python dependencies specified in [requirements.txt](backend/requirements.txt)
- Run ```cd..``` in the terminal to go back to the root directory
- Run ```cd frontend``` in the terminal
- Run ```npm install``` and ```npm run build``` respectively
- Run ```cd ..``` to go back to the root directory
- Run ```cd backend```
- Run ```python manage.py runserver``` in terminal
- Click on the link appeared in terminal to navigate to the web app.
- Enter the hotel booking details form:
- Click 'Start Scraping' button
  - Cannot scrape data that has passed. 
- The scraped data is shown as a table.
  - A user can save data as Excel by clicking 'Save Data to Excel' button
    - Data is saved as Excel in 'scraped_hotel_data' folder.
      - 'scraped_hotel_data' folder is automatically created if not exist.

