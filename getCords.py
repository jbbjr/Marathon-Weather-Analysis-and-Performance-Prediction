import pandas as pd
from geopy.geocoders import Nominatim
from tqdm import tqdm

# Load the data from the csv file
df = pd.read_csv('/Users/bennett/Documents/marathonEnvironment/analysis/locationLearningSet.csv')

# Create an instance of the geolocator
geolocator = Nominatim(user_agent="getCords")

# Define a function to get the latitude and longitude for a location
def get_lat_long(location):
    try:
        # Use geopy to get the location object
        loc = geolocator.geocode(location)
        # Extract the latitude and longitude from the location object
        lat, long = loc.latitude, loc.longitude
    except:
        # If the location cannot be found, set the latitude and longitude to None
        lat, long = None, None
    return lat, long

# Iterate over the rows of the DataFrame and geocode the locations
for i, row in tqdm(df.iterrows(), total=len(df)):
    location = row['IsFrom']
    try:
        lat, long = get_lat_long(location)
        df.at[i, 'latitude'] = lat
        df.at[i, 'longitude'] = long
    except Exception as e:
        # If an error occurs, print a message and move on to the next location
        print(f"Error geocoding location: {location}: {e}")
        continue
    finally:
        # Save the DataFrame to a CSV file
        df.to_csv('/Users/bennett/Documents/marathonEnvironment/analysis/locationLearningSetWithCords.csv', index=False)


