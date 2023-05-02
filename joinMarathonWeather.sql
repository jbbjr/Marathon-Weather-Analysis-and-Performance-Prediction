-- UPDATE `marathondb.allRaces2012_2022.racesAll`
-- SET Net_Time = NULLIF(Net_Time, 'nan') WHERE Net_Time = 'nan'

-- UPDATE `marathondb.allRaces2012_2022.racesAll`
-- SET Time = NULLIF(Time, 'nan') WHERE Time = 'nan'

-- UPDATE `marathondb.allRaces2012_2022.racesAll`
-- SET Overall = NULLIF(Overall, 'nan') WHERE Overall = 'nan'

-- UPDATE `marathondb.allRaces2012_2022.racesAll`
-- SET DivPlace = NULLIF(DivPlace, 'nan') WHERE DivPlace = 'nan'

-- UPDATE `marathondb.allRaces2012_2022.racesAll`
-- SET Sex_Div = NULLIF(Sex_Div, 'nan') WHERE Sex_Div = 'nan'

-- UPDATE `marathondb.allRaces2012_2022.racesAll`
-- SET SexPlace = NULLIF(SexPlace, 'nan') WHERE SexPlace = 'nan'

SELECT DISTINCT
  Name,
  COALESCE(Net_Time, Time) AS Time,
  Division,
  Overall,
  COALESCE(DivPlace, SPLIT(Sex_Div, '/') [OFFSET (1)]) AS DivPlace,
  COALESCE(SexPlace, SPLIT(Sex_Div, '/') [OFFSET (0)]) AS SexPlace,
  isFrom,
  Race,
  Location,
  FORMAT_DATE('%Y-%m-%d', PARSE_DATE('%B %d, %Y', Date)) as Date,
  raceKey,
  Low0_6,
  High0_6,
  Temp0_6,
  Dew0_6,
  Humidity0_6,
  HeatIndex0_6,
  WindSpeed0_6,
  WindGust0_6,
  WindDir0_6,
  WindChill0_6,
  Precipitation0_6,
  PrecipCover0_6,
  SnowDepth0_6,
  Visibility0_6,
  CloudCover0_6,
  SeaLevelPressure0_6,
  WeatherType0_6,
  Info0_6,
  Conditions0_6,
  
  Low6_12,
  High6_12,
  Temp6_12,
  Dew6_12,
  Humidity6_12,
  HeatIndex6_12,
  WindSpeed6_12,
  WindGust6_12,
  WindDir6_12,
  WindChill6_12,
  Precipitation6_12,
  PrecipCover6_12,
  SnowDepth6_12,
  Visibility6_12,
  CloudCover6_12,
  SeaLevelPressure6_12,
  WeatherType6_12,
  Info6_12,
  Conditions6_12,

  Low12_18,
  High12_18,
  Temp12_18,
  Dew12_18,
  Humidity12_18,
  HeatIndex12_18,
  WindSpeed12_18,
  WindGust12_18,
  WindDir12_18,
  WindChill12_18,
  Precipitation12_18,
  PrecipCover12_18,
  SnowDepth12_18,
  Visibility12_18,
  CloudCover12_18,
  SeaLevelPressure12_18,
  WeatherType12_18,
  Info12_18,
  Conditions12_18,

  Low18_24,
  High18_24,
  Temp18_24,
  Dew18_24,
  Humidity18_24,
  HeatIndex18_24,
  WindSpeed18_24,
  WindGust18_24,
  WindDir18_24,
  WindChill18_24,
  Precipitation18_24,
  PrecipCover18_24,
  SnowDepth18_24,
  Visibility18_24,
  CloudCover18_24,
  SeaLevelPressure18_24,
  WeatherType18_24,
  Info18_24,
  Conditions18_24

FROM (
  SELECT *,
    CONCAT(REPLACE(Race, ' ', '_'), CAST(FORMAT_DATE('%Y-%m-%d', PARSE_DATE('%B %d, %Y', Date)) AS STRING)) as raceKey
  FROM `marathondb.allRaces2012_2022.racesAll`
) AS races

LEFT JOIN (
  SELECT
    Minimum_Temperature as Low0_6, 
    Maximum_Temperature as High0_6,
    Temperature as Temp0_6,
    Dew_Point as Dew0_6,
    Relative_Humidity as Humidity0_6,
    Heat_Index as HeatIndex0_6,
    Wind_Speed as WindSpeed0_6,
    Wind_Gust as WindGust0_6,
    Wind_Direction as WindDir0_6,
    Wind_Chill as WindChill0_6,
    Precipitation as Precipitation0_6,
    Precipitation_Cover as PrecipCover0_6,
    Snow_Depth as SnowDepth0_6,
    Visibility as Visibility0_6,
    Cloud_Cover as CloudCover0_6,
    Sea_Level_Pressure as SeaLevelPressure0_6,
    Weather_Type as WeatherType0_6,
    Info as Info0_6,
    Conditions as Conditions0_6,
    CONCAT(Race, Date_time) as EMORN1weatherKey
  FROM `marathondb.weatherConsolidated.earlymorningWeatherP1`
  UNION ALL
  SELECT
    Minimum_Temperature as Low0_6, 
    Maximum_Temperature as High0_6,
    Temperature as Temp0_6,
    Dew_Point as Dew0_6,
    Relative_Humidity as Humidity0_6,
    Heat_Index as HeatIndex0_6,
    Wind_Speed as WindSpeed0_6,
    Wind_Gust as WindGust0_6,
    Wind_Direction as WindDir0_6,
    Wind_Chill as WindChill0_6,
    Precipitation as Precipitation0_6,
    Precipitation_Cover as PrecipCover0_6,
    Snow_Depth as SnowDepth0_6,
    Visibility as Visibility0_6,
    Cloud_Cover as CloudCover0_6,
    Sea_Level_Pressure as SeaLevelPressure0_6,
    Weather_Type as WeatherType0_6,
    Info as Info0_6,
    Conditions as Conditions0_6,
    CONCAT(Race, Date_time) as EMORN1weatherKey
  FROM `marathondb.weatherConsolidated.earlymorningWeatherP2`) ON EMORN1weatherKey = races.raceKey

LEFT JOIN (
  SELECT
    Minimum_Temperature as Low6_12, 
    Maximum_Temperature as High6_12,
    Temperature as Temp6_12,
    Dew_Point as Dew6_12,
    Relative_Humidity as Humidity6_12,
    Heat_Index as HeatIndex6_12,
    Wind_Speed as WindSpeed6_12,
    Wind_Gust as WindGust6_12,
    Wind_Direction as WindDir6_12,
    Wind_Chill as WindChill6_12,
    Precipitation as Precipitation6_12,
    Precipitation_Cover as PrecipCover6_12,
    Snow_Depth as SnowDepth6_12,
    Visibility as Visibility6_12,
    Cloud_Cover as CloudCover6_12,
    Sea_Level_Pressure as SeaLevelPressure6_12,
    Weather_Type as WeatherType6_12,
    Info as Info6_12,
    Conditions as Conditions6_12,
    CONCAT(Race, Date_time) as MORN1weatherKey
  FROM `marathondb.weatherConsolidated.morningWeatherP1`
  UNION ALL
  SELECT
    Minimum_Temperature as Low6_12, 
    Maximum_Temperature as High6_12,
    Temperature as Temp6_12,
    Dew_Point as Dew6_12,
    Relative_Humidity as Humidity6_12,
    Heat_Index as HeatIndex6_12,
    Wind_Speed as WindSpeed6_12,
    Wind_Gust as WindGust6_12,
    Wind_Direction as WindDir6_12,
    Wind_Chill as WindChill6_12,
    Precipitation as Precipitation6_12,
    Precipitation_Cover as PrecipCover6_12,
    Snow_Depth as SnowDepth6_12,
    Visibility as Visibility6_12,
    Cloud_Cover as CloudCover6_12,
    Sea_Level_Pressure as SeaLevelPressure6_12,
    Weather_Type as WeatherType6_12,
    Info as Info6_12,
    Conditions as Conditions6_12,
    CONCAT(Race, Date_time) as MORN1weatherKey
  FROM `marathondb.weatherConsolidated.morningWeatherP2`) ON MORN1weatherKey = races.raceKey

LEFT JOIN (
  SELECT
    Minimum_Temperature as Low12_18, 
    Maximum_Temperature as High12_18,
    Temperature as Temp12_18,
    Dew_Point as Dew12_18,
    Relative_Humidity as Humidity12_18,
    Heat_Index as HeatIndex12_18,
    Wind_Speed as WindSpeed12_18,
    Wind_Gust as WindGust12_18,
    Wind_Direction as WindDir12_18,
    Wind_Chill as WindChill12_18,
    Precipitation as Precipitation12_18,
    Precipitation_Cover as PrecipCover12_18,
    Snow_Depth as SnowDepth12_18,
    Visibility as Visibility12_18,
    Cloud_Cover as CloudCover12_18,
    Sea_Level_Pressure as SeaLevelPressure12_18,
    Weather_Type as WeatherType12_18,
    Info as Info12_18,
    Conditions as Conditions12_18,
    CONCAT(Race, Date_time) as AFT1weatherKey
  FROM `marathondb.weatherConsolidated.afternoonWeatherP1`
  UNION ALL
  SELECT
    Minimum_Temperature as Low12_18, 
    Maximum_Temperature as High12_18,
    Temperature as Temp12_18,
    Dew_Point as Dew12_18,
    Relative_Humidity as Humidity12_18,
    Heat_Index as HeatIndex12_18,
    Wind_Speed as WindSpeed12_18,
    Wind_Gust as WindGust12_18,
    Wind_Direction as WindDir12_18,
    Wind_Chill as WindChill12_18,
    Precipitation as Precipitation12_18,
    Precipitation_Cover as PrecipCover12_18,
    Snow_Depth as SnowDepth12_18,
    Visibility as Visibility12_18,
    Cloud_Cover as CloudCover12_18,
    Sea_Level_Pressure as SeaLevelPressure12_18,
    Weather_Type as WeatherType12_18,
    Info as Info12_18,
    Conditions as Conditions12_18,
    CONCAT(Race, Date_time) as AFT1weatherKey
  FROM `marathondb.weatherConsolidated.afternoonWeatherP2`) ON AFT1weatherKey = races.raceKey

LEFT JOIN (
  SELECT
    Minimum_Temperature as Low18_24, 
    Maximum_Temperature as High18_24,
    Temperature as Temp18_24,
    Dew_Point as Dew18_24,
    Relative_Humidity as Humidity18_24,
    Heat_Index as HeatIndex18_24,
    Wind_Speed as WindSpeed18_24,
    Wind_Gust as WindGust18_24,
    Wind_Direction as WindDir18_24,
    Wind_Chill as WindChill18_24,
    Precipitation as Precipitation18_24,
    Precipitation_Cover as PrecipCover18_24,
    Snow_Depth as SnowDepth18_24,
    Visibility as Visibility18_24,
    Cloud_Cover as CloudCover18_24,
    Sea_Level_Pressure as SeaLevelPressure18_24,
    Weather_Type as WeatherType18_24,
    Info as Info18_24,
    Conditions as Conditions18_24,
    CONCAT(Race, Date_time) as NIGHT1weatherKey
  FROM `marathondb.weatherConsolidated.nightWeatherP1`
  UNION ALL
  SELECT
    Minimum_Temperature as Low18_24, 
    Maximum_Temperature as High18_24,
    Temperature as Temp18_24,
    Dew_Point as Dew18_24,
    Relative_Humidity as Humidity18_24,
    Heat_Index as HeatIndex18_24,
    Wind_Speed as WindSpeed18_24,
    Wind_Gust as WindGust18_24,
    Wind_Direction as WindDir18_24,
    Wind_Chill as WindChill18_24,
    Precipitation as Precipitation18_24,
    Precipitation_Cover as PrecipCover18_24,
    Snow_Depth as SnowDepth18_24,
    Visibility as Visibility18_24,
    Cloud_Cover as CloudCover18_24,
    Sea_Level_Pressure as SeaLevelPressure18_24,
    Weather_Type as WeatherType18_24,
    Info as Info18_24,
    Conditions as Conditions18_24,
    CONCAT(Race, Date_time) as NIGHT1weatherKey
  FROM `marathondb.weatherConsolidated.nightWeatherP2`) ON NIGHT1weatherKey = races.raceKey
