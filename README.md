# Finding-the-Best-Place-to-Stay-with-Price-per-Review-from-Booking.com-using-Web-Scraping
**Finding** the **best place** to stay with **Price/Review** from Booking.com using **web-scraping** via a local **web-app**.

Aim to provide Price/Review Score of the places located in the specified city,
when finding a place to stay in that city during a trip.  

A **lower Price/Review Score** indicates that the place is **not expensive**, yet, with a **great review score**.   

## Status
Latest Update: 18 July 2024

[![CodeQL](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/codeql.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/codeql.yml)  

[![Backend Test](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/backend-test.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/backend-test.yml)

[![Frontend Test](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/frontend-test.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/frontend-test.yml)

[![Scraper Test](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/scraper-test.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/scraper-test.yml)

[![Docker Build](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/docker-build.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/docker-build.yml)

## To scrape data from Booking.com via a Local Web-App
- Download this file: [docker-compose.yml](docker-compose.yml) or clone this repo.
- Pull this Docker image: ```docker pull sakanbeer88/best-hotel-web-app-backend:latest```
- Pull this Docker image: ```docker pull sakanbeer88/best-hotel-web-app-frontend:latest```
- Run ```docker-compose up```
- Navigate to [localhost:3000](http://localhost:3000)

## Disclaimer
When filling the form, please use an abbreviation for **currency**
- For example, If the wanted currency is US Dollar, then enter USD in the currency tab.

Ticking **Scrape Hotel Properties Only** box in the form means that the scraper will scrape only places that are hotels.
If not ticked, the scraper will scrape all places available through Booking.com in the specified city.