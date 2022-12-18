import os
from google.cloud import bigquery
import pandas as pd

# set credentials (json key file that gives access to BigQuery)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"json key file path"
client = bigquery.Client()

# query the entire table that has weather data joined to marathon data
request = client.query(
    """
    SELECT * FROM `table`
    """
)

# ensures query is completed
results = request.result()

# query results to pandas df
df = results.to_dataframe()

# send off to folder for Excel cleaning and analysis in R
dir = r'path .csv'
df.to_csv(dir)
print('done')
