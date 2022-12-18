import os
from google.cloud import bigquery
import pandas as pd

# set credentials (json key file that gives access to BigQuery)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\jbbla\OneDrive\Documents\joinedMarathonSets\marathonweather-3d428cf9330a.json"
client = bigquery.Client()

# query the entire table that has weather data joined to marathon data
request = client.query(
    """
    SELECT * FROM `marathonweather.racesWithWeather.marathons2021V2`
    """
)

# ensures query is completed
results = request.result()

# query results to pandas df
df = results.to_dataframe()

# send off to folder for Excel cleaning and analysis in R
dir = r'C:\Users\jbbla\OneDrive\Documents\joinedMarathonSets\analysis2021.csv'
df.to_csv(dir)
print('done')
