import pandas as pd
import glob

# races are saved as individual files, we need to create a single file for race results in a year before we send to BigQuery
files = glob.glob(r'path//*.csv')

allRaces = pd.DataFrame()

# iterate through each race and concatenate until completion 
for file in files:
    df = pd.read_csv(file)
    allRaces = pd.concat([allRaces, df])

    
# create the file and then upload to BigQuery
dir = r"path"
allRaces.to_csv(dir)

print(allRaces.head)
print("Complete Conversion")

    

