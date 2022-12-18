-- Queries the necesarry data needed to gather weather data for a given year

SELECT DISTINCT
FORMAT_DATE('%Y-%m-%d', PARSE_DATE('%B %d, %Y', Date)) as Date, 
REPLACE(Race, " ", "_") as Race, 
Location    
 FROM `marathonweather.allRaces.races2019Clean`