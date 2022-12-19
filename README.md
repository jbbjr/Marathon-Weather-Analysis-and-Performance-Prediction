# Marathon Weather Analysis and Performance Prediction

The marathon, a 26.2 mile race that is enjoyed by runners and spectators from all across the globe. Not only is the marathon a widly popular endurance sport, but it is highly competitive. A lot of attention the sport gets tends to center around records and the athletes who break them. With this in mind, one can only imagine - *What does it take to break a record? How do you do it?* - 

As an avid marathoner, myself and others know how much preparation goes into a running a single race. What we also understand is that there are a lot of externalities that are involved. Many things we can prepare for prior, such as the elevation gain or overall difficulty of a course. We know that these can effect our times, but we can also ready ourselves to perform despite their presence. But there are also externalities we can never anticipate. One of these is the weather. Sure, it may generally be warmer in one location, windier in another. But despite normalities in weather, there is still a lot of variation that can occur. The question is, just how much can that variation impact a runners performance? To uncover the causal relationship between the two, I am proposing a **Multi-Way Fixed Effects Model** which will control for runner fixed effects and time fixed effects.

## Organization of Project
- Marathon Data Collection and Manipulation
- Weather Data Colleciton and Manipulation
- Finalizing our Data
- Modeling
- Interpretation and Visualization

## Marathon Data Collection and Manipulation
Gathering the marathon data requires one large task: **Web Scraping**.
