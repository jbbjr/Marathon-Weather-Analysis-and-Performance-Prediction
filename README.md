# Marathon Weather Analysis and Performance Prediction

The marathon, a 26.2-mile race that is enjoyed by runners and spectators across the globe. The sport is wildly popular and hyper competitive. Most of the attention it receives tends to center around records and the athletes who break them. As an avid marathoner, myself and others understand the amount of training required to prepare for a single race. Furthermore, we understand there are variables that can affect our performance. There variables we can train in preparation for, such as altitude or overall difficulty of a course. However, there are some variables that occur on race day which we have no control over. One of these is the weather. While there are general weather trends in certain locations, there is still a lot of variation that can occur. The question is, just how much can that variation impact a runner’s performance? To try and uncover the causal relationship between the two, I am proposing a multi-way fixed effects model to control for variation in runners, races, and time. The dataset is composed of data scraped from MarathonGuide (an online marathon database accredited by the BAA that consists of marathon results dating back to 2000, for races in English speaking parts of the world) and historical weather data gathered from a weather API called Visual Crossing.

<br/><br/>
<br/><br/>

# Organization of Project

- Case Study: Boston (2023)
- Hypothesis
- Building the Marathon Dataset
- Contructing the Database
- Collecting Appropriate Weather Data
- Data Manipulation and Finalizing the Dataset
- Modeling
- Interpretation and Visualization
- Conclusion

<br/><br/>
<br/><br/>

<img align="right" width="500" src="https://www.wnct.com/wp-content/uploads/sites/99/2023/04/643f0950359698.51111723.jpeg?strip=1">






# Case Study: (Boston 2023)
Pictured on the right is the elite mens pool from the Boston Marathon (2023), with Eliud Kipchoge leading the front of the pack. Kipchoge is regarded as the GOAT of the marathon. 
### Eliud Kipchoge
- Unofficially broke the 2:00:00 barrier
- Currently holds the world record of 2:01:09, Berlin (2022)

All eyes were on Kipchoge April, 2023 when he came to Boston. Many expected a 1st place finish with a good margin of error, and maybe even a course record. However, this was far from the case. 

After pushing the pace until mile 20, Kipchoge hit the imfamous wall. He ended up finishing 6th, with a time of 2:09:43. 

As of now there is much speculation about what might've gone wrong. Many say it was the fact that he missed a fuel bottle at the final station. Others believe he underestimated the course, as he never actually practiced the course and only rode it once. Kipchoge claims that a leg injury at mile 18 foiled his attempt. Furthermore, the weather was absolutely brutal this year.

### Conditions
- Temperature:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;48°F
- Humidity:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;99%
- Windspeed:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;10mph
- Conditions:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;rain

It's likely that all of these had a play in Kipchoge's performance at Boston. Now the question is, how can we quantify the impact of the weather given these circumstances?

<br/><br/>
<br/><br/>

# Hypothesis
From my marathoning / running experience, I've expereciend a wide range of weather conditions. Furthermore, I'm under the belief that there's likely an optimal range of temperatures to run a race in. To explore this idea, look at the two graphs below. The graphs below display a distribution of finishing times from the Boston and Fort Smith Marathon, respectively. In the legend, you'll see the year and average temperature at for the race.

| <img src="https://github.com/jbblancojr/Marathon-Weather-Analysis-and-Performance-Prediction/raw/main/images/output.png" alt="Image 1" style="max-width: 100%;"> | <img src="https://github.com/jbblancojr/Marathon-Weather-Analysis-and-Performance-Prediction/raw/main/images/output2.png" alt="Image 2" style="max-width: 100%;"> |
| :---: | :---: |

### Things to notice from these distributions
- When the Boston Marathon was 70°F in 2018, the average finishing time was around 30 minutes slower
- When the Fort Smith Marathon was 25°F in 2018, the average finishing time was around 30 minutes slower as well
- Average finishing times when the temperature is in the 40°F zone seem to be faster 

To confirm this hypothesis we will need to test joint significance of temperature and its quadratic when we construct our model. 

It will look something like this:

$H_0: \beta_{temperature} = \beta_{temperature^2} = 0$

$H_a: \beta_{temperature} \neq 0, \beta_{temperature^2} \neq 0$

<br/><br/>
<br/><br/>

# Building the Marathon Dataset
The first obvious step to this analysis is finding the appropriate marathon data to pair some weather data with. Fortunately, a lot of the aggregation of marathon data is already accessible. [MarathonGuide.com](http://www.marathonguide.com/index.cfm) is a database housing 100% of marathons occuring in the English speaking world from 2000 to present day, and their results. Since there is an immense amount of data on this site, we can build a web scraper to automate most of the collection process and format it for our use case

To scrape data from the site, we can implement `autoScrape`, which utilizes Selenium and Pandas. 

This often takes 2-3 days to get the entire year, so I typically run this on a linux server and use **TMUX** to scrape multiple years at once

### `autoScrape` in summary:
- Input a year and for that given year: the script creates the URL that contains a years worth of marathon URLs
- Create a list of the marathon URLs and iterate through them
- For each URL 
  - Find the amount of columns and their titles by XPATH
  - Locate the data that is on the page by XPATH and append it to a df  
  - If an XPATH for a more results button exists, click it 
- When the more results button no longer exists, convert the df to a csv and put it in a folder
- Move to next race and repeat until completion

Once this is complete, we can create a database in BigQuery with all of our csv files. 

<br/><br/>
<br/><br/>

# Constructing the Database
Now that we have all the necesarry marathon data in csvs, we need to create a database out of them. This will help us later when we need to relate it to the weather data we collect in the next step. We'll be creating our database in Google Cloud and work with BigQuery

Retrospectively, I would likely have combined this with the webscraper and uploaded tables to datasets rather save as csvs, but oh well :)

### `createDB` in summary:
- For the year folders created
  - Create a dataset of that year if not present
  - For each race in the year
    - Create a table of the race if not present

This happens pretty quickly. For the 11 years I've scraped it took about an hour or so. This would make sense given that this is O(n<sup>2</sup>) worst case and the webscraper is something like O(n<sup>3</sup>) best case.

<br/><br/>
<br/><br/>

# Collecting Appropriate Weather Data
Now that the marathon data is set up in our database we need to collect the appropriate information to help us collect the necessary weather data for our analysis. 

This only requires one simple query. Here's an exmaple of the query for the year 2012. Ultimately we just write this a few times for however many years we have and use **UNION ALL** to get everything in the same query. After this is done, we can save the output as a csv and return to Python to get the weather data we need.
```
SELECT DISTINCT FORMAT_DATE('%Y-%m-%d', PARSE_DATE('%B %d, %Y', Date)) as Date, REPLACE(Race, " ", "_") as Race, Location  
FROM `marathondb.scrapedRaces2012.*` 
```
### Additional Query Information
- The Date variable we scraped is displayed as *July, 28, 2013*, and we are simply formatting it to *2013-06-28* to meet API syntax requirements.
- Along with the date, we need the location of a race so that we can get the right weather data.
- Lastly, we need the race so we know which row to send our weather data back to. We will use it for formatting a key in a few steps.

Once we return to Python we just need to format all our results csv to meet query syntax requirements for the weather API. We will need to make a request for each observation in our csv so we can write a script to autmoate this process for us. Additionally, we will need to divide the time in the day for modeling purposes. This will result in 4 weather tables, based on quarters of the day.

### `vcRequests` in summary:
- Read query results
- Create lists for Dates, Locations, and Races
- Create an empty dataframe
- Pick a quarter of the day. (00:00-06:00, 06:00-12:00, 12:00-18:00, 18:00-24:00)
- For every observation
  - Format it to meet API syntax requirements
  - Request the data for that quarter of the day
  - Append the data to the empty dataframe and attach the Race name
- Send the dataframe to a csv

When this finishes, we need to send the four csvs back to the database. All we need to do is scale `createDB` to make one job and upload them as tables to a newly created weather dataset.

<br/><br/>
<br/><br/>

# Data Manipulation and Finalizing the Dataset
Now we have both our marathon and weather data finalized in our database. We now need to find a way to relate everything and send it over to **Stata** to do some modeling. 

### What's left
- Relate the datasets
- Eliminate null values
- Store results as a csv

Similar to how we utilize the Google Cloud API to send things to BigQuery, we can open up a client in Python and make requests. This makes it so we can do the rest of the job in one script.

### Final Dataset Query in summary:
- Select distinct obsevations from our marathon dataset
- Create a key for each observation to help identify which weather data corresponds to it: (key = Race_Loation_Date)
- Left join the weather data back to the marathon data based on the key
- Eliminate any rows where a column has a missing observation

This query happens inside the Python script, so we can store the results as a dataframe and then convert it to a csv.

<br/><br/>
<br/><br/>





