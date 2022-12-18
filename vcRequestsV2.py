import pandas as pd

# Properties for API Requests 
BaseURL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history'

# three lists representative of three columns of data
dt = []
loc = []
race = []


# holds each individual weather query
temp_df = []

# holds all weather queries combined
main_df = pd.DataFrame()


# a file that represents a query of all distinct instaces of (Dates, Locations, Races). Date and Location for finding historical weather values, Race for joining the weather data back in BigQuery
distinct_vals = pd.read_csv(r'path')

# lists Date, Location, Race that we can iterate through for weather API queries 
dt = distinct_vals['Date'].values.tolist()
loc = distinct_vals['Location'].values.tolist()
race = distinct_vals['Race'].values.tolist()
 
# alters Location to meet weather API query syntax requirements
for i in range(len(dt)):
    loc[i] = loc[i].replace() # usually a few things need to change depending on the year, fix anything here with .replace method

# iterate through all Date, Location, Race values until completion 
for i in range(len(dt)):
    # if you set a variable equal to the query request with values you want to use the replace method on, the pull will fail
    # aggregateHours=24 (allows one query per date and location, in time window of specified startDateTune and endDateTime)
    # dt[i] = Date that corresponds with query
    # loc[i] = Location that corresponds with the query    
    query = BaseURL + '?aggregateHours=24&startDateTime=' + dt[i] + 'T00:00:00&endDateTime=' + dt[i] + 'T23:00:00&unitGroup=us&location=' + loc[i] + '&contentType=csv&key=KEY'
    
    # get the individual query into a temporary df     
    temp_df = pd.read_csv(query) 
    
    # tack on the corresponding race, which will be used to join back the data in BigQuery     
    temp_df.insert(len(temp_df.columns), "Race", race[i])
    
    # concatinate the query with the key back to the main df     
    main_df = pd.concat([main_df, temp_df])
   
# send our compiled pull request to a csv
dir = r'path'
main_df.to_csv(dir)

print('Pull request complete!')




    


