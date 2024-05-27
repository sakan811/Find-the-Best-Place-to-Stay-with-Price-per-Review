# Finding-the-Best-Place-to-Stay-with-Price-per-Review-from-Booking.com-using-Web-Scraping
Finding the Best Place to Stay with Price per Review from Booking.com using Web Scraping.  

Aim to provide places with Price/Review Score when finding a place to stay during a trip.  

A lower Price/Review Score indicates that the place isn't expensive, yet, with a great review score.   

## Status
[![CodeQL](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/codeql.yml)  
[![Python application](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/sakan811/Find-the-Best-Place-to-Stay-with-Price-per-Review/actions/workflows/python-app.yml)

## To scrape data from Booking.com
- Go to [main.py](main.py)
- Adjust these variables as needed:
  - Must enter every variable to make the process work properly.
    - city
    - check_in (format: yyyy-mm-dd)
    - check_out (format: yyyy-mm-dd)
    - group_adults (number of adults)
    - num_rooms (number of room) 
    - group_children (number of children)
    - selected_currency
    - hotel_filter (Set to True if wanting to scrape only hotel properties data, else scrape all property data)
      - Example:    
      ```python
      city = 'London'
      check_in = '2024-12-22'
      check_out = '2024-12-23'
      group_adults = '2'
      num_rooms = '1'
      group_children = '0'
      selected_currency = 'GBP'
      hotel_filter = True
      ```
- Run the script.
  - Data is saved as Excel.
