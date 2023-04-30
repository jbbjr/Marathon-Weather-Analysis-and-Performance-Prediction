# Marathon Weather Analysis and Performance Prediction

The marathon, a 26.2-mile race that is enjoyed by runners and spectators across the globe. The sport is wildly popular and hyper competitive. Most of the attention it receives tends to center around records and the athletes who break them. As an avid marathoner, myself and others understand the amount of training required to prepare for a single race. Furthermore, we understand there are variables that can affect our performance. There variables we can train in preparation for, such as altitude or overall difficulty of a course. However, there are some variables that occur on race day which we have no control over. One of these is the weather. While there are general weather trends in certain locations, there is still a lot of variation that can occur. The question is, just how much can that variation impact a runner’s performance? To try and uncover the causal relationship between the two, I am proposing a multi-way fixed effects model to control for variation in runners, races, and time. The dataset is composed of data scraped from MarathonGuide (an online marathon database accredited by the BAA that consists of marathon results dating back to 2000, for races in English speaking parts of the world) and historical weather data gathered from a weather API called Visual Crossing.

# Organization of Project

- Overview
- Data Sources
- Building the Weather Dataset
- Contructing the Database
- Collecting Appropriate Weather Data
- Data Manipulation and Finalizing the Dataset
- Modeling
- Interpretation and Visualization
- Conclusion
<br/><br/>
<br/><br/>
<img align="right" width="500" src="https://www.wnct.com/wp-content/uploads/sites/99/2023/04/643f0950359698.51111723.jpeg?strip=1">






## Overview
Pictured on the right is the elite mens pool from the Boston Marathon (2023), with Eliud Kipchoge leading the front of the pack. Kipchoge is regarded as the GOAT of the marathon. 
### Eliud Kipchoge
- Unofficially broke the 2:00:00 barrier
- Currently holds the world record of 2:01:09, Berlin (2022)

All eyes were on Kipchoge April, 2023 when he came to Boston. Many expected a 1st place finish with a good margin of error, and maybe even a course record. However, this was far from the case. 

After pushing the pace until mile 20, Kipchoge hit the imfamous wall. He ended up finishing 6th with a time of 2:09:43. As of now there is much speculation about what might've gone wrong. Many say it was the fact that he missed a fuel bottle at the final station. Others believe he underestimated the course, as he never actually practiced the course and only rode it once. Kipchoge claims that a leg injury at mile 18 foiled his attempt. Furthermore, the weather was absolutely brutal this year.

### Conditions
- Temperature:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;48°F
- Humidity:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;99%
- Windspeed:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;10mph
- Conditions:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;rain

It's likely that all of these had a play in Kipchoge's performance at Boston. Now the question is, how can we quantify the impact of the weather given these circumstances?
