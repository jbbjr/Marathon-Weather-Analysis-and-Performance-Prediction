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
From my marathoning / running experience, I've expereciend a wide range of weather conditions. Furthermore, I'm under the belief that there's likely an optimal range of temperatures to run a race in. To explore this idea, look at the two graphs below. These graphs display a distribution of finishing times from the Boston and Fort Smith Marathon, respectively. In the legend, you'll see the year and average temperature at for the race.

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

Once we return to Python we just need to format all our results csv to meet query syntax requirements for the weather API. For this part, we can use the [Visual Crossing](https://www.visualcrossing.com/) weather API, which has data for weather just about anywhere on the globe, dating back to 100 years. 

Since our API can only process one request per query, we will need to make a query for each individual observation in our csv. We can write a script to autmoate this process for us. Additionally, we will need to divide the time in the day for modeling purposes. This will result in 4 weather tables, based on quarters of the day.

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

# Modeling
Now that we have the data we need, we'll leverage some econometrics to find a causal relationship between the finishing times and the weather. With what we have, the best we can do is implement some fixed effects to try and mitigate some bias. 

### Runner Fixed Effect
We can create a runner fixed effect by identifying individuals in the dataset that we observed over time. There will be some things within a runner such as innate ability that remains fixed across time, so the runner fixed effect will help us exploit that variation without needing to explicity observe it in the model. 

### Race Fixed Effect
We also will want to create a race fixed effect by utilizing our race column. This is useful because the Race variable will capture things such as course difficulty, elevation gain, altitude, or other related variables that remain fixed across time. Additionally, since we have a large set of locations with different weather patterns and ranges of possible temperatures, the race variable does a great job of controlling for seasonality (because they always happen around the same time of the year), as well as limiting variation to what would actually be feasible in the given locaiton. 

### Time Fixed Effect
Lastly, we would want to create a time fixed effect by creating a year value, which we can strip from the date. There will be things that effect all races and runners equally on a given year and the year fixed effect allows us to acknowledge that without biasing our results (ex. Covid).

## Regression Results
In a real econometrics article we would include a model of OLS and one for each fixed effect combination. This is so that we can discuss potential bias in the model. I've uploaded each regression output in the project branch, but I'll only touch on OLS and our final multi-way fixed effects model here in the readme.

### OLS

OLS doesn't really tell us anything as we aren't exploiting any variation. Our key variables of interest are temp6_12 and tempSQ (highlighted). Since our coefficient is negative for temperature, meaning that as temperature increases, runners become faster, we can be certain that there is some bias in the model because this is not the sign we would expect. Additionally, because of this bias we cannot tell anything from the quadratic term.

``` stata
reg seconds age isMale temp6_12sq overall divplace sexplace temp0_6 temp6_12 temp12_18 temp18_24 
dew0_6 dew6_12 dew12_18 dew18_24 humidity0_6 humidity6_12 humidity12_18 humidity18_24 
windspeed0_6 windspeed6_12 windspeed12_18 windspeed18_24 precipitation0_6 precipitation6_12 
precipitation12_18 precipitation18_24 snowdepth0_6 snowdepth6_12 snowdepth12_18 snowdepth18_24 
cloudcover0_6 cloudcover6_12 cloudcover12_18 cloudcover18_24

      Source |       SS           df       MS      Number of obs   = 2,700,351
-------------+----------------------------------   F(34, 2700316)  =  27234.31
       Model |  1.0717e+13        34  3.1521e+11   Prob > F        =    0.0000
    Residual |  3.1254e+13 2,700,316  11574085.1   R-squared       =    0.2553
-------------+----------------------------------   Adj R-squared   =    0.2553
       Total |  4.1971e+13 2,700,350  15542763.5   Root MSE        =    3402.1

------------------------------------------------------------------------------------
           seconds | Coefficient  Std. err.      t    P>|t|     [95% conf. interval]
-------------------+----------------------------------------------------------------
         "temp6_12 |  -1063.504   15.87246   -67.00   0.000    -1094.613   -1032.395"
       "temp6_12sq |   2.983099   .0174215   171.23   0.000     2.948954    3.017245"
               age |   34.06994   .1880986   181.13   0.000     33.70127     34.4386
            isMale |  -1608.826   5.239671  -307.05   0.000    -1619.096   -1598.557
           overall |   .0870705   .0007693   113.18   0.000     .0855627    .0885783
          divplace |  -.3618438   .0038143   -94.86   0.000    -.3693198   -.3543678
          sexplace |   .1738191   .0015264   113.88   0.000     .1708274    .1768108
           temp0_6 |   1103.079   9.363336   117.81   0.000     1084.727    1121.431
         temp12_18 |  -235.3364   12.95616   -18.16   0.000      -260.73   -209.9428
         temp18_24 |   194.6448    4.63798    41.97   0.000     185.5545    203.7351
            dew0_6 |  -1220.037   9.566712  -127.53   0.000    -1238.787   -1201.286
           dew6_12 |   1110.962   16.06264    69.16   0.000      1079.48    1142.444
          dew12_18 |  -64.11778   12.49461    -5.13   0.000    -88.60678   -39.62878
          dew18_24 |  -116.6003   4.122549   -28.28   0.000    -124.6803   -108.5202
       humidity0_6 |   535.7708    3.93068   136.30   0.000     528.0668    543.4748
      humidity6_12 |  -477.8091   6.942032   -68.83   0.000    -491.4153    -464.203
     humidity12_18 |   44.52776   5.871409     7.58   0.000        33.02    56.03551
     humidity18_24 |   69.61203   2.380405    29.24   0.000     64.94652    74.27754
      windspeed0_6 |  -132.8742    1.35247   -98.25   0.000     -135.525   -130.2234
     windspeed6_12 |   90.32539   1.709239    52.85   0.000     86.97534    93.67544
    windspeed12_18 |   41.81243   1.231101    33.96   0.000     39.39952    44.22535
    windspeed18_24 |  -14.26038   .6937654   -20.56   0.000    -15.62013   -12.90062
  precipitation0_6 |  -.5777545   21.53051    -0.03   0.979    -42.77679    41.62128
 precipitation6_12 |  -1466.304    27.6017   -53.12   0.000    -1520.403   -1412.206
precipitation12_18 |  -513.5358   18.84825   -27.25   0.000    -550.4777   -476.5939
precipitation18_24 |   833.1807   10.44521    79.77   0.000     812.7085     853.653
      snowdepth0_6 |  -11.15256   15.69873    -0.71   0.477    -41.92151     19.6164
     snowdepth6_12 |  -509.7127   349.8516    -1.46   0.145     -1195.41    175.9842
    snowdepth12_18 |   4562.219   480.6803     9.49   0.000     3620.103    5504.336
    snowdepth18_24 |  -4041.062   239.5948   -16.87   0.000    -4510.659   -3571.464
     cloudcover0_6 |   12.34796   .2980359    41.43   0.000     11.76382     12.9321
    cloudcover6_12 |  -34.52718   .5262155   -65.61   0.000    -35.55855   -33.49582
   cloudcover12_18 |   .5638832   .5556662     1.01   0.310     -.525203    1.652969
   cloudcover18_24 |   9.709904   .3475835    27.94   0.000     9.028653    10.39116
             _cons |   5969.679   87.97727    67.85   0.000     5797.246    6142.111
------------------------------------------------------------------------------------
```

### Multi-Way Fixed Effects

Once we run our fixed effects, we get a better idea of the effect of the temperature. We find that for every 1°F increase, the average finishing time for an individuals marathon increases by 106 seconds on average, holding all else constant (Cetaris Paribus). 

```stata
reghdfe seconds age isMale temp6_12sq overall divplace sexplace temp0_6 temp6_12 temp12_18 
temp18_24 dew0_6 dew6_12 dew12_18 dew18_24 humidity0_6 humidity6_12 humidity12_18 humidity18_24 
windspeed0_6 windspeed6_12 windspeed12_18 windspeed18_24 precipitation0_6 precipitation6_12 
precipitation12_18 precipitation18_24 snowdepth0_6 snowdepth6_12 snowdepth12_18 snowdepth18_24 
cloudcover0_6 cloudcover6_12 cloudcover12_18 cloudcover18_24, 
absorb(raceID runnerID year)

(dropped 707 singleton observations)
(MWFE estimator converged in 16 iterations)

HDFE Linear regression                            Number of obs   =  1,642,185
Absorbing 3 HDFE groups                           F(  34,1244417) =   11744.38
                                                  Prob > F        =     0.0000
                                                  R-squared       =     0.7926
                                                  Adj R-squared   =     0.7263
                                                  Within R-sq.    =     0.2429
                                                  Root MSE        =  2049.1911

------------------------------------------------------------------------------------
           seconds | Coefficient  Std. err.      t    P>|t|     [95% conf. interval]
-------------------+----------------------------------------------------------------
         "temp6_12 |   106.3919   15.95486     6.67   0.000      75.1209    137.6628"
       "temp6_12sq |   1.071027   .0198147    54.05   0.000     1.032191    1.109863"
               age |   33.43476   .3693746    90.52   0.000      32.7108    34.15872
            isMale |  -1083.079   36.65458   -29.55   0.000    -1154.921   -1011.238
           overall |   .1578759   .0010311   153.11   0.000     .1558549     .159897
          divplace |   .1006977   .0042485    23.70   0.000     .0923709    .1090245
          sexplace |   .1542226   .0019596    78.70   0.000     .1503819    .1580633
           temp0_6 |  -38.46225   9.266626    -4.15   0.000    -56.62452   -20.29998
         temp12_18 |  -272.8644    13.0169   -20.96   0.000    -298.3771   -247.3517
         temp18_24 |   103.4986   4.903797    21.11   0.000     93.88735    113.1099
            dew0_6 |   64.88545   9.483993     6.84   0.000     46.29715    83.47375
           dew6_12 |  -239.4708   15.82593   -15.13   0.000    -270.4891   -208.4525
          dew12_18 |    318.594   12.21134    26.09   0.000     294.6602    342.5279
          dew18_24 |  -136.9102   4.306018   -31.80   0.000    -145.3498   -128.4706
       humidity0_6 |  -41.75705   3.910367   -10.68   0.000    -49.42124   -34.09286
      humidity6_12 |   110.2884   6.885749    16.02   0.000     96.79253    123.7842
     humidity12_18 |  -140.7867    5.85131   -24.06   0.000    -152.2551   -129.3183
     humidity18_24 |   70.61606   2.458117    28.73   0.000     65.79823    75.43388
      windspeed0_6 |  -15.99174   1.443453   -11.08   0.000    -18.82086   -13.16262
     windspeed6_12 |   14.69561   1.839387     7.99   0.000     11.09047    18.30074
    windspeed12_18 |   5.333335   1.290633     4.13   0.000     2.803738    7.862931
    windspeed18_24 |   8.423932   .6802589    12.38   0.000     7.090648    9.757216
  precipitation0_6 |   234.0194   20.05804    11.67   0.000     194.7063    273.3325
 precipitation6_12 |  -234.8266   25.72512    -9.13   0.000     -285.247   -184.4062
precipitation12_18 |   209.3994   18.23993    11.48   0.000     173.6498     245.149
precipitation18_24 |   -282.022   9.856378   -28.61   0.000    -301.3401   -262.7038
      snowdepth0_6 |   117.3391   27.17448     4.32   0.000     64.07806    170.6002
     snowdepth6_12 |  -111.4945   417.3846    -0.27   0.789    -929.5541    706.5651
    snowdepth12_18 |  -1.574619   561.5132    -0.00   0.998    -1102.121    1098.972
    snowdepth18_24 |   31.13829   245.2376     0.13   0.899    -449.5191    511.7957
     cloudcover0_6 |   2.005489   .2871415     6.98   0.000     1.442701    2.568276
    cloudcover6_12 |  -3.229763   .4979031    -6.49   0.000    -4.205636    -2.25389
   cloudcover12_18 |   1.470228    .546621     2.69   0.007     .3988697    2.541587
   cloudcover18_24 |  -.1459595   .3616966    -0.40   0.687    -.8548725    .5629534
             _cons |   14396.46   105.6101   136.32   0.000     14189.47    14603.45
------------------------------------------------------------------------------------

Absorbed degrees of freedom:
-----------------------------------------------------+
 Absorbed FE | Categories  - Redundant  = Num. Coefs |
-------------+---------------------------------------|
      raceID |       743           0         743     |
    runnerID |    396982           1      396981     |
        year |        11           1          10    ?|
-----------------------------------------------------+


```

### Joint Significance

Additionally, we can run a joint significance test in stata to see if our hypothesis is true. 

```stata
test temp6_12 temp6_12sq

 ( 1)  temp6_12 = 0
 ( 2)  temp6_12sq = 0

       F(  2,1244417) = 1551.83
            Prob > F =    0.0000
```

This confirms our initial hypothesis and if we look at the sign, we see that as temperature increases, time will increase at an increasing rate. On the latter, we can infer that as temperature decreases, time will decrease at a decreasing rate.

<br/><br/>
<br/><br/>

# Conclusion
To wrap things up, here's what we've done so far:

- Constructed a database of marathon and weather data by leveraging
  - Web scraping
  - Various API packages
- Constructed an unbalanced panel dataset with SQL
- Leveraged econometric techniques to run multiple regressions
- Discovered the existence of an optimal range of temperature for running a marathon
- Quantified the effect of a 1°F increase on marathon finishing times (Still likely overpredicting)

As of now this is a great start, but there is still lots of work to be done! To anyone who comes across this, I am always open to suggestions on how to further improve any of these processes.   


