import pandas as pd
from math import radians, sin, cos, sqrt, atan2

# read csv
df = pd.read_csv('../db/location_dataset.csv')

def calculate_distance(lat1, long1, lat2, long2):
    # return ((lat1-lat2)**2 + (long1-long2)**2)**0.5
        # Radius of the Earth in kilometers
    R = 6371.0
    
    # Convert latitude and longitude from degrees to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(long1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(long2)
    
    # Differences in coordinates
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    # Calculate distance
    distance = R * c
    return distance

# print(df)
# fmipa lat long
lat = -7.767638
long = 110.376639

# calculate distance from location_name to fmipa
df['distance'] = df.apply(lambda row: calculate_distance(lat, long, row['latitude'], row['longitude']), axis=1)

# choose location_name == 'UGM'
df = df[df['location_name'] == 'UGM']
# calculate distance from location_name to fmipa
df['distance'] = df.apply(lambda row: calculate_distance(lat, long, row['latitude'], row['longitude']), axis=1)

print(df['distance'])