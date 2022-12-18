-- cleans up the scrape results a bit, to reduce some redundancy when we reach Excel stage

CREATE TABLE `allRaces.racesClean` AS (
  
-- Organize table and consolidate columns that had different names but same data on website
WITH racesCleaned AS (
  SELECT Last_Name__First_Name__Sex_Age_ AS Name, 
  COALESCE(Net_Time, CAST(Time as String)) AS OfficialTime,
  OverAll_Place AS Overall,
  SPLIT(Sex_Place___Div_Place, '/') [OFFSET (1)] AS DivPlace,
  COALESCE(CAST(Sex_Place AS String), SPLIT(Sex_Place___Div_Place, '/') [OFFSET (0)]) AS SexPlace,
  DIV,
  COALESCE(City__State__Country, City__Country, State__Country, City__State, Country, State, City) AS IsFrom,
  Country,
  City__State__Country,
  City__Country,
  City__State,
  City,
  State__Country,
  State,

  Date,
  Location,
  Race,
  BQ_ as BQ,

  FROM `allRaces.racesRAW`   
)

-- remove repeat rows, (site always has to show 100 results per page, so some results get pulled twice on the last page) 
  SELECT DISTINCT * FROM racesCleaned WHERE OfficialTime is not null
)