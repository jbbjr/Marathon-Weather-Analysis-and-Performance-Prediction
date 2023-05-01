

import os
from google.cloud import bigquery
import pandas as pd

# set credentials (json key file that gives access to BigQuery)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'PATH/dbKey.json'
client = bigquery.Client()

# query the entire table that has weather data joined to marathon data

request = client.query(
     """
     QUERY
     """
)


# ensures query is completed
results = request.result()

# query results to pandas df
df = results.to_dataframe()

# send off to folder

df.to_csv(path)
print('done')
