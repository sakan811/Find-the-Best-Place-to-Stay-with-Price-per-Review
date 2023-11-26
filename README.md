# Finding-the-Best-Place-to-Stay-with-Price-per-Review-from-Booking.com-using-Web-Scraping
Finding the Best Place to Stay with Price per Review from Booking.com using Web Scraping.  

Aim to provide places with Price/Review Score when finding a place to stay during a trip.  

A lower Price/Review Score indicates that the place is inexpensive, yet, with a great review score.   

# Code
- Adjust these variables as needed:
  - city
  - check_in (format: yyyy-mm-dd)
  - check_out (format: yyyy-mm-dd)
  - group_adults (number of adults)
  - num_rooms (number of room) 
  - group_children (number of children)
  - selected_currency
    - Example:    
    ```python
    city = 'London'
    check_in = '2023-12-22'
    check_out = '2023-12-23'
    group_adults = '2'
    num_rooms = '1'
    group_children = '0'
    selected_currency = 'GBP'
    ```
- Scraping from the website.
- Save data as Excel.
