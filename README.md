# Finding the Best Place to Stay with Price per Review from Booking.com using Web-Scraping
**Finding** the **best place** to stay with **Price/Review** from Booking.com using **web-scraping** via a local **web-app**.

Aim to provide **Price/Review Score** of the places located in the specified city,
when finding a place to stay in that city during a trip.  

A **lower Price/Review Score** indicates that the place is **not expensive**, yet, with a **great review score**.   

## Status
Latest Update: 6 August 2024

[![CodeQL](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/codeql.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/codeql.yml)  

[![Backend Test](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/backend-test.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/backend-test.yml)

[![Frontend Test](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/frontend-test.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/frontend-test.yml)

[![Scraper Test](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/scraper-test.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/scraper-test.yml)

[![Docker Build](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/docker-build.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/docker-build.yml)

## To Use the Web-App
### Setup the Web App
- Download [docker-compose.yml](docker-compose.yml) file and place it in any directory of your choice.
- Find your **User Agent**:
  - Go to https://www.whatismybrowser.com/detect/what-is-my-user-agent/
  - Enter your User Agent into **USER_AGENT** environment variable inside [docker-compose.yml](docker-compose.yml)
- Execute:
  ```
  docker-compose up
  ```
  
## Access the Web App
- Navigate to [http://localhost:5000/](http://localhost:5000/)
- Press **Ctrl + C** in the terminal or **stop** the Docker container to stop the web app.

## Disclaimer
When filling the form, please use an abbreviation for **currency**
- For example, If the wanted currency is US Dollar, then enter USD in the currency tab.

Ticking **Scrape Hotel Properties Only** box in the form means that the scraper will scrape only places that are hotels.
If not ticked, the scraper will scrape all places available through Booking.com in the specified city.

# Codebase Detail
[Click here](docs/DOCS.md) to read a brief docs of this codebase.