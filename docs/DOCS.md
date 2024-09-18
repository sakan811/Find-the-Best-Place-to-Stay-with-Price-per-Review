# Brief Document
## Backend
[logging_config.py](..%2Fbackend%2Flogging_config.py)
- Logger config
- You can set log level in this script:
    ```
    main_logger = configure_logging_with_file(log_dir='logs', log_file='main.log', logger_name='main', level="INFO")
    ```

### Django App
* [views.py](..%2Fbackend%2Fapp%2Fviews.py)
  * Contain API endpoints

* [urls.py](..%2Fbackend%2Fapp%2Furls.py)
  * API endpoints routing

* [models.py](..%2Fbackend%2Fapp%2Fmodels.py)
  * Contain SQLite table schema

### [app_func](..%2Fbackend%2Fapp%2Fapp_func) Package
- [utils_func.py](..%2Fbackend%2Fapp%2Fapp_func%2Futils_func.py)
  - Contain Django App utility functions

- [db_func.py](..%2Fbackend%2Fapp%2Fapp_func%2Fdb_func.py)
  - Contain Django database-related functions

### Django
* [settings.py](..%2Fbackend%2Fdjango_project%2Fsettings.py)
    * Django settings

* [urls.py](..%2Fbackend%2Fdjango_project%2Furls.py)
  * Define URL pattern for API

### [scraper](..%2Fbackend%2Fscraper) Package
* [graphql_scraper.py](..%2Fbackend%2Fscraper%2Fgraphql_scraper.py)
  * Contain Scraper dataclass and its methods to scrape data.

### [scraper_func](..%2Fbackend%2Fscraper%2Fscraper_func) Package
* [data_extractor.py](..%2Fbackend%2Fscraper%2Fscraper_func%2Fdata_extractor.py)
  * Contain functions for extracting the desired data

* [data_transformer.py](..%2Fbackend%2Fscraper%2Fscraper_func%2Fdata_transformer.py)
  * Contain functions for transforming data in the Pandas Dataframe.

* [graphql_func.py](..%2Fbackend%2Fscraper%2Fscraper_func%2Fgraphql_func.py)
  * Contain functions related to GraphQL request and response.

* [utils.py](..%2Fbackend%2Fscraper%2Fscraper_func%2Futils.py)
  * Contain utility functions

## Frontend
[App.jsx](..%2Ffrontend%2Fsrc%2FApp.jsx)
* Define routes for each webpage

[HotelTable.jsx](..%2Ffrontend%2Fsrc%2Fcomponents%2FHotelTable.jsx)
* React component for the webpage that shows hotel data as a table
  * Contain functions, as buttons, for saving data as an Excel, and redirecting to the Form page 

[ScrapingForm.jsx](..%2Ffrontend%2Fsrc%2Fcomponents%2FScrapingForm.jsx)
* React component for the Form page
  * Contain the form to enter booking details and a function, as a button, 
    to submit the data and send POST request to the API endpoint 
    to save data to the database.