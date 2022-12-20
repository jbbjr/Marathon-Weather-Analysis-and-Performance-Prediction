# Marathon Weather Analysis and Performance Prediction

The marathon, a 26.2 mile race that is enjoyed by runners and spectators from all across the globe. Not only is the marathon a widly popular endurance sport, but it is highly competitive. A lot of attention the sport gets tends to center around records and the athletes who break them. With this in mind, one can only imagine - *What does it take to break a record? How do you do it?* - 

As an avid marathoner, myself and others know how much preparation goes into a running a single race. What we also understand is that there are a lot of externalities that are involved. Many things we can prepare for prior, such as the elevation gain or overall difficulty of a course. We know that these can effect our times, but we can also ready ourselves to perform despite their presence. But there are also externalities we can never anticipate. One of these is the weather. Sure, it may generally be warmer in one location, windier in another. But despite normalities in weather, there is still a lot of variation that can occur. The question is, just how much can that variation impact a runners performance? To uncover the causal relationship between the two, I am proposing a **Multi-Way Fixed Effects Model** which will control for runner fixed effects and time fixed effects.

## Organization of Project
- [Terminology](https://github.com/jbblancojr/Marathon-Weather-Analysis-and-Performance-Prediction/edit/main/README.md#terminology)
- [Marathon Data Collection and Manipulation](https://github.com/jbblancojr/Marathon-Weather-Analysis-and-Performance-Prediction/edit/main/README.md#marathon-data-collection-and-manipulation)
- [Weather Data Colleciton and Manipulation](https://github.com/jbblancojr/Marathon-Weather-Analysis-and-Performance-Prediction/edit/main/README.md#weather-data-colleciton-and-manipulation)
- [Finalizing our Data](https://github.com/jbblancojr/Marathon-Weather-Analysis-and-Performance-Prediction/edit/main/README.md#finalizing-our-data)
- Modeling
- Interpretation and Visualization

## Terminology
This section is intended for readers unfamiliar with programming or econometric fundimentals. (you can probably skip this)

#### Programming 
- **Python**: 
  - A general purpose open source programming language. 
  - For our use case, it helps us collect data and semi-automate the process.
- **Structured Query Language (SQL)**: 
  - For our use case, we can manipulate and organize all or large portions of our data at once. BigQuery is Google's "version" SQL.
- **API**:
  - Application Programming Interface.
  - For our use case, we ask the API for certain things with code and it returns them to us.  
- **Pandas**:
  - A software library that helps us extrapolate and analyze data.
- **Selenium**:
  - A software library that allows us to automate a webdriver by writing code.
- **df**:
  - A Pandas dataframe (essentially a very maluable Excel sheet).
- **XPATH**:
  - A line of code refrencing a piece of a website.
  - For our use case, this may be a button to click, or a cell in a table.
- **Function**:
  - A few lines of code that complete a specific task (like an Excel formula).
- **Database**
  - A collection of datasets (like an Excel file).
- **Dataset**
  - A collection of tables (Excel sheets). 
#### Econometrics
- **Fixed Effect**:
  - stuff 

## Marathon Data Collection and Manipulation
Gathering the marathon data requires one large task: **Web Scraping**. Fortunately, a lot of the aggregation of marathon data is already accessible. [MarathonGuide.com](http://www.marathonguide.com/index.cfm) is a database housing 100% of marathons and their results in the English speaking world, from 2000 to present day. However, to perform analysis on the data, it needs to be scraped and formatted for our use case. 

To scrape data from the site, we can implement `autoScrape`, which utilizes Selenium and Pandas.

### `autoScrape` in summary:
- Input a URL that contains a years worth of marathon URLs
- Create a list of the marathon URLs and iterate through them
- For each URL 
  - Find the amount of columns and their titles by XPATH
  - Locate the data on that is on the page by XPATH and append it to a df  
  - If a more results button XPATH exists, click it 
- When the more results button no longer exists, convert the df to a csv and put it in a folder
- Move to next race and repeat until completion

Once a year is scraped, we end up with a folder conaining CSV files for each individual race in a given year. To combine all of the races into one file we quickly run the `fileJoin` script. This just creates a CSV housing the data for an entire year of races. We then send this off to our BigQuery database for some additional cleaning and querying.

### BigQuery
Now that our marathon data is in our database, we can query `yearCleaner` to quickly remove some rows and columns we won't need and do some reformatting of data that got scraped weird. After this, we need to get our weather data.

## Weather Data Colleciton and Manipulation
Now that we have marathon data in BigQuery, we need to collect the weather data that is associated with it. This is a little more complicated than just looking up the weather and adding it to the database. We won't actually have to find weather data for each individual instance of a runner, just for the race. This should make intuitive sense (the weather is the same for everyone who runs the race).

Here is what we need to do:
- Find each Race that occured
- The location the race occured in
- The date the race occured on

To do this we can utilize `distinctDateLoc` to query a table of these instances. We then export the results as a CSV and go back to Python to gather our weather data.

Now that we're back in Python we need to access the [Visual Crossing](https://www.visualcrossing.com/) weather API. To complete this task we will use `vcRequests`, which collects all the necesarry weather data for a year of marathons by reading through the CSV file we created from `distinctDateLoc`. 

### Pulling from the API
To gather our weather data we need to send requests to the Visual Crossing API. If formatted correctly, it returns us the data in the requested format. We can temporarily store the data in a df and then send it to a CSV file. Since Visual Crossing can only send us one instance of weather data per request, we need to write some code to get all the necesarry weather data for the year into one CSV.    

### Formatting the Request
Here is an example of a query request. It's kind of like a link to a website. We give it to the Visual Crossing API, and it looks it up and returns the results to us! 
```
https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history?
aggregateHours=24&startDateTime=2019-05-13T00:00:00&endDateTime=2019-05-13T23:00:00&unitGroup=us
&location=Portland,ME,USA&contentType=csv&key=APIKEY'
```
This query is requesting data for:
- The average of all weather metrics (aggregateHours=)
  - on March 13, 2019 from 12:00 AM to 11:59 PM (start/endDateTime=)
  - in Portland, Maine (location=)
- Saved as a CSV (contentType=)
- In US units (unitGroup=)
- Using my account (key=)

All we have to do is send a bunch of these to the Visual Crossing API and it will give us the weather data for all of our races. `vcRequests` can do this for us automatically.

### `vcRequests` in summary:
- Read the CSV file that `distinctDateLoc` created
- Create lists of Dates, Locations, and Races 
- For each Date, Location, and Race, format the query
  - Format the query
  - Query the corresponding weather data   
  - Append the data to a df

When this is complete, we end up with a CSV file of weather data that corresponds to each row of our `distinctDateLoc` CSV. Now it's time to head back to BigQuery and finalize our data.  

## Finalizing our Data
hey!





