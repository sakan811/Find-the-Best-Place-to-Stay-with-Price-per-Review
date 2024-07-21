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
- In the command line terminal, run ```chmod +x setup.sh``` and ```./setup.sh``` respectively.
- Get the values from Booking.com:
  - Go to Booking.com, and perform a search for any location with any booking details.
  - Right-click anywhere on the webpage and select **Inspect** to open the developer tools.
  - Navigate to the **Network** tab.
  - Scroll through the network requests until you find one with a name starting with **graphql?ss=**.
  - Click on this request and navigate to the **Headers** tab.
  - Find the values for the following headers and enter them into your **.env** file:
    - User-Agent ➡ USER_AGENT
    - X-Booking-Csrf-Token ➡ X_BOOKING_CSRF_TOKEN
    - X-Booking-Context-Action-Name ➡ X_BOOKING_CONTEXT_ACTION_NAME
    - X-Booking-Context-Aid ➡ X_BOOKING_CONTEXT_AID
    - X-Booking-Et-Serialized-State ➡ X_BOOKING_ET_SERIALIZED_STATE
    - X-Booking-Pageview-Id ➡ X_BOOKING_PAGEVIEW_ID
    - X-Booking-Site-Type-Id ➡ X_BOOKING_SITE_TYPE_ID
    - X-Booking-Topic ➡ X_BOOKING_TOPIC
- Navigate to the **backend** directory
  - Run ```python manage.py runserver```
- Navigate to the **frontend** directory
  - Run ```npm start```
- Navigate to [localhost:3000](http://localhost:3000)

## Disclaimer
When filling the form, please use an abbreviation for **currency**
- For example, If the wanted currency is US Dollar, then enter USD in the currency tab.

Ticking **Scrape Hotel Properties Only** box in the form means that the scraper will scrape only places that are hotels.
If not ticked, the scraper will scrape all places available through Booking.com in the specified city.