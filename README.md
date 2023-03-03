# Marathon Weather Analysis and Performance Prediction

The marathon, a 26.2 mile race that is enjoyed by runners and spectators from all across the globe. Not only is the marathon a widly popular endurance sport, but it is highly competitive. A lot of attention the sport gets tends to center around records and the athletes who break them. With this in mind, one can only imagine - *What does it take to break a record? How do you do it?* - 

As an avid marathoner, myself and others know how much preparation goes into a running a single race. What we also understand is that there are a lot of externalities that are involved. Many things we can prepare for prior, such as the elevation gain or overall difficulty of a course. We know that these can effect our times, but we can also ready ourselves to perform despite their presence. There are also externalities we can never anticipate. One of these is the weather. Sure, it may generally be warmer in one location, or windier in another. But despite normalities in weather, there is still a lot of variation that can occur. The question is, just how much can that variation impact a runners performance? To uncover the causal relationship between the two, I am proposing a **Multi-Way Fixed Effects Model** which will control for runner fixed effects, time fixed effects, and race fixed effects.

## Organization of Project
- Interpretation and Visualization
- Terminology
- Marathon Data Collection and Manipulation
- Weather Data Collection and Manipulation
- Creating Additional Variables with Existing Data
- Finalizing our Data
- Modeling
- Interpretation and Visualization
- Conclusion

## Terminology
This section is intended for readers unfamiliar with programming or econometric fundimentals. (you can probably skip this)

#### Programming 
- **Python**: 
  - A general purpose, open source programming language. 
  - For our use case, it helps us collect data and semi-automate the process.
- **Structured Query Language (SQL)**: 
  - For our use case, we can manipulate and organize all or large portions of our data at once. 
  - BigQuery is Google's "version" SQL.
- **API**:
  - Application Programming Interface.
  - For our use case, we ask the API for certain things with code and the API will return them to us.  
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
- tbd

## Marathon Data Collection and Manipulation
Gathering the marathon data requires one large task: **Web Scraping**. Fortunately, a lot of the aggregation of marathon data is already accessible. [MarathonGuide.com](http://www.marathonguide.com/index.cfm) is a database housing 100% of marathons occuring in the English speaking world from 2000 to present day, and their results. To perform analysis on all of this data, it needs to be scraped and formatted for our use case. 

To scrape data from the site, we can implement `autoScrape`, which utilizes Selenium and Pandas.

### `autoScrape` in summary:
- Input a URL that contains a years worth of marathon URLs
- Create a list of the marathon URLs and iterate through them
- For each URL 
  - Find the amount of columns and their titles by XPATH
  - Locate the data that is on the page by XPATH and append it to a df  
  - If an XPATH for a more results button exists, click it 
- When the more results button no longer exists, convert the df to a csv and put it in a folder
- Move to next race and repeat until completion

Once a year is scraped, we end up with a folder conaining CSV files for each individual race in a given year. To combine all of the races into one file, we quickly run the `fileJoin` script. This just creates a CSV housing the data for an entire year of races. We then send this CSV off to our BigQuery database for some additional cleaning and querying.

### BigQuery
Now that our marathon data is in our database, we can query `yearCleaner` to quickly remove some rows and columns we won't need, as well as reformat some of the data that got scraped weird. After this, we need to get our weather data.

## Weather Data Colleciton and Manipulation
Now that we have marathon data in BigQuery, we need to collect the weather data that is associated with it. This is a little more complicated than just looking up the weather data and adding it to the database. We need to access the [Visual Crossing](https://www.visualcrossing.com/) weather API, which has data for weather just about anywhere on the globe, dating back to 100 years. 

For our use case, we won't actually have to find weather data for each individual instance of a runner, just for the race. This should make intuitive sense (the weather is the same for everyone who runs the race).

Here is what we need to do:
- Find each Race that occured
- The location the race occured in
- The date the race occured on

To do this we can utilize `distinctDateLoc` to query a table of these instances. We then export the results as a CSV and go back to Python to gather our weather data.

Once we're back in Python, we need to write some code to access Visual Crossings API. To complete this task we will use `vcRequests`, which collects all the necesarry weather data for a year of marathons by reading through the CSV file we created from `distinctDateLoc`. 

### Pulling from the API
Gathering weather data requires sending requests to the Visual Crossing weather API. If formatted correctly, it returns us the requested weather data.

### Formatting the Request
Here is an example of a query request. It's kind of like a link to a website. We give it to the API, the API looks it up, and then it will return the results to us. 
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

Visual Crossing can only send us one instance of weather data per request. So all we have to do is send a bunch of these to the Visual Crossing weather API and it will give us the weather data for all of our races. `vcRequests` can do this for us automatically.

### `vcRequests` in summary:
- Read the CSV file that `distinctDateLoc` created
- Create lists of Dates, Locations, and Races 
- For each Date and Location, format the query
  - Format the query
  - Query the corresponding weather data
  - Add the correspond Race to the weather data (we will need this later)
  - Append the data to a df

When this is complete, we end up with a CSV file of weather data that corresponds to each row of our `distinctDateLoc` CSV. Then it's just a matter of going back to BigQuery and finalizing our data.

## Finalizing our Data
Now we have our marathon data and the corresponding weather data in BigQuery, the next step is to combine it so we can conduct analyses and start modeling. 

To finalize the data for the given year we need to do two things:
- Run the `weatherJoin` query to connect the marathon and weather data
  >  - This performs a left join with our marathon data and weather data. 
  >    - Meaning, weather data fills out wherever the marathon race matches the weather race. 
  >    - (This is why we included Race earlier in `vcRequests`)
- Use `bqRequests` to get the finalized data from BigQuery to a CSV so we can do some modeling.
  >  - Similar to `vcRequests`, we are asking the BigQuery API to send us our tables so we can
  >    - Put them in a df
  >    - And then send them to a CSV file

Once this is done, we have the necessary data to conduct analyses on a year of marathons. This entire process just needs to be repeated for every year of marathon data available on MarathonGuide. 

## Creating Additional Variables with Existing Data
After all the data has been collected and compiled, there is still a lot than can be done with existing data to build new variables. To control for variation in runners, we may want to look at where they're from, their age, or gender. Most of the races provide us with this data, but each race entry form is different so we end up with many overlapping age groups and partial adresses. The most difficult of these to address is the location column.

### Building the CountryOfOrigin Variable
Most of our data has partial location information to tell us where a runner is from. However, some of these may only include a city or a smaller region within a country. We need to find a way to generalize this to the country someone is from so it can be utilized in the modelling stage. We can back into this information with help from some additional APIs.

### Backing into Country
in the `yearCleaner` query, we consolidated all of our location information into one column. This creates a comma delimited string value depending on what the entry form looked like for the given race. 

Examples of variation in the isFrom column:
- Greensboro, NC
- Calgary
- Paris, France
- Boston, MA, USA

We want the rightmost value so we can quickly run a line of code on a df of our dataset to build a new column which we will call *broadest*.

Here's what happens when we run `df['broadest'] = df['IsFrom'].apply(lambda x: x.rsplit(',', 1)[-1].strip())` on the examples above.
- NC
- Calgary
- France
- USA

This works great on the bottom two, but we still need to drill back up further for the rest. We'll put this column to the side for now and return to it later.

WIP

In this section I'll be transitioning over to **Stata** for some data wrangling

## Modeling
The modeling stage is currently a work in progress. I have some general ideas with the data that I've compiled.

#### Runner Variables we have:
- Official Time (measured in seconds) | *Independent Variable*
- Overall Place
- Division Place
- Sex Place
- Division
- Gender
- Country
- Race Location
- Race Name

#### Weather Variables we have:
- Min Temp (the low for the day)
- Max Temp (the high for the day)
- Average Over 24 hours for: 
  - Temperature | *Explanatory Variable of Interest*
  - Dew Point 
  - Humidity (%)
  - Heat Index
  - Wind Speed
  - Wind Gust
  - Wind Direction
  - Wind Chill
  - Precipitation
  - Precipitation Cover
  - Snow Depth
  - Visibility
  - Cloud Cover
  - Weather Type


#### An idea for a model:

$$officialtime_{it} = \beta_{0} + \beta temperature_{it} + \beta race_{it} + \beta runner_{it} + \beta year_{t}  + a_{i} + \mu_{it}$$

- where *i* represents a unique combination of a given runner at a given race and $a_{i}$ captures unobserved factors that vary across runners and races, but are fixed across time. For runners, we might want to control for biological factors or location factors that may give an advantage in a marathon finishing time. For races, we might want to control for the difficulty or altitude of the course, as well as how well renowned the race is (which would attract faster runners)
- $year_{t}$ represents the given year a race was run and captures variations across time, but not across runners or races


#### Things I'd be interested in adding would be:
- relevant weather variables correlated with temperature
- A $temperature^2$ variable. I'm pretty certain there is a most optimal temperature, and we could use this quadratic to find that
- International (a dummy variable, takes a value of 1 if Country != Country of Race Location)
- inclusion of a runners gender, age division, and country they reside in 
- Utilization of Random Forest or a Decision Tree to categorize runner locations into countries, rather than states or cities 

This model is a rough sketch. The data is ready, but I need to collaborate with my professors to ensure the unbiasedness of the model / what variables to include.

Additionally. The data currently scraped:
- Raw data for years 2017, 2016
- Cleaned data paired with weather 2019-2022 (in the model) (n ~1,000,000)

*Note: The end goal is to conduct analysis on all 22 years, but I wanted to get something up with what I currently have gathered. I'll certainly have a model finalized this Spring semester, and adding additional data can be an ongoing process as time goes on.*

