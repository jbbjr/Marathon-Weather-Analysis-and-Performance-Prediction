import pandas as pd
from geopy.geocoders import Nominatim
from tqdm import tqdm

# Load the data from the csv file
df = pd.read_csv('/Users/bennett/Documents/marathonEnvironment/analysis/locationLearningSetWithCords.csv')

# Create an instance of the geolocator
geolocator = Nominatim(user_agent="getCountry")

# Define a function to get the country for a latitude and longitude
def get_country(lat, long):
    try:
        # Use geopy to get the location object
        loc = geolocator.reverse(f"{lat}, {long}")
        # Extract the country from the location object
        country = loc.raw['address'].get('country')
    except:
        # If the country cannot be found, set it to None
        country = None
    return country

# Iterate over the rows of the DataFrame and get the country for each latitude and longitude
for i, row in tqdm(df.iterrows(), total=len(df)):
    lat = row['latitude']
    long = row['longitude']
    try:
        country = get_country(lat, long)
        df.at[i, 'country'] = country
    except Exception as e:
        # If an error occurs, print a message and move on to the next location
        print(f"Error getting country for lat, long: {lat}, {long}: {e}")
        continue
    finally:
        # Save the DataFrame to a CSV file
        df.to_csv('/Users/bennett/Documents/marathonEnvironment/analysis/locationLearningSetWithCountryENG.csv', index=False)
