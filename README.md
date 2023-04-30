# Marathon Weather Analysis and Performance Prediction

The marathon, a 26.2-mile race that is enjoyed by runners and spectators across the globe. The sport is wildly popular and hyper competitive. Most of the attention it receives tends to center around records and the athletes who break them. As an avid marathoner, myself and others understand the amount of training required to prepare for a single race. Furthermore, we understand there are variables that can affect our performance. There variables we can train in preparation for, such as altitude or overall difficulty of a course. However, there are some variables that occur on race day which we have no control over. One of these is the weather. While there are general weather trends in certain locations, there is still a lot of variation that can occur. The question is, just how much can that variation impact a runner’s performance? To try and uncover the causal relationship between the two, I am proposing a multi-way fixed effects model to control for variation in runners, races, and time. The dataset is composed of data scraped from MarathonGuide (an online marathon database accredited by the BAA that consists of marathon results dating back to 2000, for races in English speaking parts of the world) and historical weather data gathered from a weather API called Visual Crossing.

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

# Hypothesis
Here you'll see two distributions graphs. On the left is the Boston marathon...

## Building the Marathon Dataset
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

# Constructing the Database
Now that we have all the necesarry marathon data in csvs, we need to create a database out of them. This will help us later when we need to relate it to the weather data we collect in the next step. Retrospectively, I would likely have combined this with the webscraper and uploaded tables to datasets rather save as csvs, but oh well :)

### `createDB` in summary:
- For the year folders created
  - Create a dataset of that year if not present
  - For each race in the year
    - Create a table of the race if not present

This happens pretty quickly. For the 11 years I've scraped it took about an hour or so. This would make sense given that this is O(n<sup>2</sup>) worst case and the webscraper is something like O(n<sup>3</sup>) best case.

# Collecting Appropriate Weather Data
Now that the marathon data is set up in our database we need to collect the appropriate information to help us collect the necessary weather data for our analysis. 

This only requires one simple query. Here's an exmaple of the query for the year 2012. Ultimately we just write this a few times for however many years we have and use **UNION ALL** to get everything in the same query.
```
SELECT DISTINCT FORMAT_DATE('%Y-%m-%d', PARSE_DATE('%B %d, %Y', Date)) as Date, REPLACE(Race, " ", "_") as Race, Location  
FROM `marathondb.scrapedRaces2012.*` 
```
### Additional Query Information
- The Date variable we scraped is displayed as *July, 28, 2013*, and we are simply formatting it to *2013-06-28* to meet API syntax requirements.
- Along with the date, we need the location of a race so that we can get the right weather data.
- Lastly, we need the race so we know which row to send our weather data back to. We will use it for formatting a key in a few steps.

After this is done, we can save the output as a csv and return to python to get the weather data we need.




