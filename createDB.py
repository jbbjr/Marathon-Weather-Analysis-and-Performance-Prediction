import os
from google.cloud import bigquery
from tqdm import tqdm
import re

# set credentials (json key file that gives access to BigQuery)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'JSONKEY'

# create client object
client = bigquery.Client(project='marathondb')

# project_id = 'marathondb'

job_config = bigquery.LoadJobConfig(
    autodetect=True,
    skip_leading_rows=1,
    allow_quoted_newlines=True,
    source_format=bigquery.SourceFormat.CSV,
)


for year in range(2012, 2023):
    year_folder = os.path.join('PATH', f"scrapedRaces{year}")
    dataset_id = f'scrapedRaces{year}'
    # create the dataset first time through
    try: 
        client.get_dataset(dataset_id)
    except:
        client.create_dataset(f'marathondb.{dataset_id}')
    # Iterate through all CSV files in the folder
    for file in tqdm(os.listdir(year_folder)):
        table = ''
        if file.endswith(".csv"):
            file_path = os.path.join(year_folder, file)
            table = os.path.splitext(os.path.basename(file_path))[0]
            table = re.sub(r'[^\w]+', '', table).lower()
            if table[0].isdigit():
                table = '_' + table
            try:
                client.get_table(f'marathondb.{dataset_id}.{table}')
                print(f'{dataset_id}.{table} already exists')
            except:
                client.create_table(f'marathondb.{dataset_id}.{table}')
                with open(file_path, 'rb') as source_file:
                    job = client.load_table_from_file(
                        source_file,
                        f'marathondb.{dataset_id}.{table}',
                        job_config=job_config
                    )
                    job.result()
                    print(f'{job.output_rows} rows uploaded to {dataset_id}.{table}.')
