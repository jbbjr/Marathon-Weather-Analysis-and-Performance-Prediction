# Marathon Weather Analysis and Performance Prediction

The marathon, a 26.2 mile race that is enjoyed by runners and spectators from all across the globe. Not only is the marathon a widly popular endurance sport, but it is highly competitive. A lot of attention the sport gets tends to center around records and the athletes who break them. With this in mind, one can only imagine - *What does it take to break a record? How do you do it?* - 

As an avid marathoner, myself and others know how much preparation goes into a running a single race. What we also understand is that there are a lot of externalities that are involved. Many things we can prepare for prior, such as the elevation gain or overall difficulty of a course. We know that these can effect our times, but we can also ready ourselves to perform despite their presence. But there are also externalities we can never anticipate. One of these is the weather. Sure, it may generally be warmer in one location, windier in another. But despite normalities in weather, there is still a lot of variation that can occur. The question is, just how much can that variation impact a runners performance? To uncover the causal relationship between the two, I am proposing a **Multi-Way Fixed Effects Model** which will control for runner fixed effects and time fixed effects.

## Organization of Project
- [Terminology](https://github.com/jbblancojr/Marathon-Weather-Analysis-and-Performance-Prediction/edit/main/README.md#terminology)
- [Marathon Data Collection and Manipulation](https://github.com/jbblancojr/Marathon-Weather-Analysis-and-Performance-Prediction/edit/main/README.md#marathon-data-collection-and-manipulation)
- [Weather Data Colleciton and Manipulation](https://github.com/jbblancojr/Marathon-Weather-Analysis-and-Performance-Prediction/edit/main/README.md#weather-data-colleciton-and-manipulation)
- Finalizing our Data
- Modeling
- Interpretation and Visualization

## Terminology
This section is intended for readers unfamiliar with programming or econometric fundimentals. (you can probably skip this)
<dl>
  <dt>Python</dt>
  <dd>A general purpose open source programming language.</dd>
  <dd>For our use case, it helps us collect data and semi-automate the process.</dd>
  <dt>SQL</dt>
  <dd>Structured Query Language</dd>
  <dd>BigQuery is Google's "version" SQL</dd> 
  <dd>For our use case, we can manipulate and organize all or large portions of our data at once</dd> 
  <dt>API</dt>
  <dd>Application Programming Interface</dd>
  <dd>For our use case, we ask the API for certain things with code and it returns them to us</dd>
  <dt>Pandas</dt>
  <dd>A software library that helps us extrapolate and analyze data</dd>
  <dt>Selenium</dt>
  <dd>A software library that allows us to automate a webdriver by writing code</dd>
  <dt>df</dt>
  <dd>a Pandas dataframe (essentially a very maluable Excel sheet)</dd>
  <dt>XPATH</dt>
  <dd>a line of code is equal to a piece of a website</dd>
  <dd>For our use case, this may be a button to click, or a cell in a table</dd>
  <dt>Function</dt>
  <dd>a few lines of code that complete a specific task (like an Excel formula)</dd>
</dl>

## Marathon Data Collection and Manipulation
Gathering the marathon data requires one large task: **Web Scraping**. Fortunately, a lot of the aggregation of marathon data is already accessible. [MarathonGuide.com](http://www.marathonguide.com/index.cfm) is a database housing 100% of marathons and their results in the English speaking world, from 2000 to present day. However, to perform analysis on the data, it needs to be scraped and formatted for our use case. 

To scrape data from the site, I created `autoScrape`, which utilizes Selenium and Pandas.

### `autoScrape` in summary:
- Input a URL that contains a years worth of marathon URLs
- Create a list of the marathon URLs and iterate through them
- For each URL, find the amount of columns and their titles by XPATH
- For the URL, use table cells XPATH to collect the data by that is on the page and append it to a df...  If a more results XPATH exists, click it. 
- When the more results button no longer exists, convert the df to a csv and put it in a folder
- Move to next race and repeat until completion

Once a year is scraped, we end up with a folder conaining CSV files for each individual race in a given year. To combine all of the races into one file I wrote a quick `fileJoin` script which simply creates a CSV housing the data for an entire year of races. We then send this off to BigQuery for some additional cleaning and querying.

### BigQuery
Now that our marathon data is into BigQuery, we can query `yearCleaner` to quickly remove some rows and columns we won't need and do some reformatting of data that got scraped weird. After this, we need to get our weather data.

## Weather Data Colleciton and Manipulation





