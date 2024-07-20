# Finding-the-Best-Place-to-Stay-with-Price-per-Review-from-Booking.com-using-Web-Scraping
**Finding** the **best place** to stay with **Price/Review** from Booking.com using **web-scraping** via a local **web-app**.

Aim to provide Price/Review Score of the places located in the specified city,
when finding a place to stay in that city during a trip.  

A **lower Price/Review Score** indicates that the place is **not expensive**, yet, with a **great review score**.   

## Status
Latest Update: 21 July 2024

[![CodeQL](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/codeql.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/codeql.yml)  

[![Backend Test](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/backend-test.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/backend-test.yml)

[![Frontend Test](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/frontend-test.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/frontend-test.yml)

[![Scraper Test](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/scraper-test.yml/badge.svg)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/scraper-test.yml)

## To scrape data from Booking.com via a Local Web-App
- Clone this repo: https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review.git
- Adjust a project path to the **backend** directory
- Install all dependencies listed in [requirements.txt](backend%2Frequirements.txt)
  - Create a **.env** file with the following variables:
    ```
    USER_AGENT=
    CSRF_TOKEN=
    CONTEXT_ACTION_NAME=
    CONTEXT_AID=
    ET_SERIALIZED_STATE=
    PAGEVIEW_ID=
    SITE_TYPE_ID=
    TOPIC=
    UA_PLATFORM=
    ORIGIN=
    PRIORITY=
    SEC_CH_UA=
    FETCH_DEST=
    FETCH_MODE=
    FETCH_SITE=
    ```
  - Check the network console of Booking.com and enter these variables as appear on the console.
- Adjust a project path to the **frontend** directory
  - Run ```npm install```
- Adjust a project path to the **backend** directory
  - Run ```python manage.py runserver```
- Adjust a project path to the **frontend** directory
  - Run ```npm start```
- Navigate to [localhost:3000](http://localhost:3000)

## Disclaimer
When filling the form, please use an abbreviation for **currency**
- For example, If the wanted currency is US Dollar, then enter USD in the currency tab.

Ticking **Scrape Hotel Properties Only** box in the form means that the scraper will scrape only places that are hotels.
If not ticked, the scraper will scrape all places available through Booking.com in the specified city.