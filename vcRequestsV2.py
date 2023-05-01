import pandas as pd
from tqdm import tqdm

print("starting")

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

time = input("select time frame to observe (emorn, morn, aft, night): ")

start = ''
end = ''

if time == "emorn":
    start = 'T00:00:00'
    end = 'T06:00:00'
elif time == "morn":
    start = 'T06:00:00'
    end = 'T12:00:00'
elif time == 'aft':
    start = 'T12:00:00'
    end = 'T18:00:00'
elif time == 'night':
    start = 'T18:00:00'
    end = 'T23:00:00'
else:
    start = 'T00:00:00'
    end = 'T23:00:00'

    

# a file that represents a query of all distinct instaces of (Dates, Locations, Races). Date and Location for finding historical weather values, Race for joining the weather data back in BigQuery
# distinct_vals = pd.read_csv(r'/Users/bennett/Documents/marathonEnvironment/weatherRequests.csv')
distinct_vals = pd.read_csv('/Users/bennett/Documents/weatherData/missing_emornALTER.csv')

# lists Date, Location, Race that we can iterate through for weather API queries 
dt = distinct_vals['Date'].values.tolist()
loc = distinct_vals['Location'].values.tolist()
race = distinct_vals['Race'].values.tolist()
 
# alters Location to meet weather API query syntax requirements
for i in range(len(dt)):
    loc[i] = str(loc[i])
    # loc[i] = str(loc[i].replace('USA', ',USA').replace('Canada', ',Canada').replace(' ', '').replace('Decon','Devon').replace('GrandCayman,CaymanIslands', 'KY1-1100').replace('HiltonHead','HiltonHeadIsland').replace('CatalinaIsland', 'Avalon').replace('Meeman-ShelbyStatePark', 'Millington').replace('TwenteAirport', 'Enschede').replace('HyaktoTanner', 'Tanner').replace('PortOrchard', 'Bremerton').replace('StHelier,Jersey', 'SaintHelier').replace('Surrey', 'Guildford').replace('WestSussex', 'Chichester').replace('Cheshire', 'LittleBudworth').replace('OuterBanks', 'KillDevilHills').replace('RNASYoevilton', 'Yeovilton').replace('MtHood', 'HoodRiver').replace('TumonBay','Dededo').replace('Snowdonia', 'Rhiwbryfdir').replace('PoipuBeachKauai', 'Poipu').replace('KeyWest', '33040').replace('UnicoiStatePark', 'Helen').replace('KingGeorgeIsland,Antarctica', '-62.033,-58.35').replace('Connemara', 'Galway').replace('Pembrokeshire,UnitedKingdom', 'Pembrokeshire,Wales').replace('LincolnandSelwyn', 'Lincoln').replace('EllsworthMountains,Antarctica','-78.7500,-85.0000').replace('Dorset','Bournemouth').replace('LonePine','Independence')) 
# iterate through all Date, Location, Race values until completion 
for i in tqdm(range(len(dt))):
    try:
        # if you set a variable equal to the query request with values you want to use the replace method on, the pull will fail
        query = BaseURL + '?aggregateHours=24&startDateTime=' + dt[i] + f'{start}&endDateTime=' + dt[i] + f'{end}&unitGroup=us&location=' + loc[i] + '&contentType=csv&key=MFSYXWD9DZQCB6CJ33W45TXFH'
        
        temp_df = pd.read_csv(query) 
        temp_df.insert(len(temp_df.columns), "Race", race[i])
        main_df = pd.concat([main_df, temp_df])
    except:
        print(f'ERROR for {loc[i]} on {dt[i]} for {race[i]}')

# send our compiled pull request to a csv
# main_df.to_csv(f'/Users/bennett/Documents/weatherData/weatherALL_{time}.csv')
main_df.to_csv(f'/Users/bennett/Documents/weatherData/weatherALL_{time}V2.csv')

print('Pull request complete!')




    


