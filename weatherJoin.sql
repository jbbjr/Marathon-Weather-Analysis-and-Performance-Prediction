-- left joins the weather table with the existing marathon data for a given year, on key = Race 

CREATE TABLE `racesWithWeather.table` AS (
SELECT * FROM `allRaces.raceClean`
LEFT JOIN (
  SELECT * EXCEPT(Race, Name), Race as racename FROM `yearlyWeather.weather`
) ON REPLACE(racename, '_', ' ') = `allRaces.racesClean`.Race
) 