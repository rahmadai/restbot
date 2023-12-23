import pandas as pd
from math import radians, sin, cos, sqrt, atan2

# C1 = number of review -> jumlah_review
# C2 = price -> average_price
# C3 = rating -> rating
# C4 = type -> restoran_type
# C5 = distance -> calculate distance from user location to restaurant location

# fmipa lat long
lat = -7.767638
long = 110.376639

weight_C1 = 5
weight_C2 = 3
weight_C3 = 5
weight_C4 = 4
weight_C5 = 2

total_weight = weight_C1 + weight_C2 + weight_C3 + weight_C4 + weight_C5

weight_param_C1 = weight_C1 / total_weight
weight_param_C2 = weight_C2 / total_weight
weight_param_C3 = weight_C3 / total_weight
weight_param_C4 = weight_C4 / total_weight
weight_param_C5 = weight_C5 / total_weight

def weighted_product(C1, C2, C3, C4, C5):
    return (C1**weight_param_C1) * (C2**(-1*weight_param_C2)) * (C3**weight_param_C3) * (C4**weight_param_C4) * (C5**(-1*weight_param_C5))

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

# read csv
global df
# df = pd.read_csv('../db/list.csv')

def preprocessing(df):
    # cleaning category if ', ' then replace with ','
    df['kategori'] = df['kategori'].apply(lambda x: x.replace(', ', ','))
    # lowercase all category
    df['kategori'] = df['kategori'].apply(lambda x: x.lower())
    # split kategori column if there are multiple categories by comma
    # df['kategori'] = df['kategori'].apply(lambda x: x.split(','))

    return df

def filter(df):
    # filter by kategori kolom if kategori have list some X
    df = df[df['kategori'].apply(lambda x: 'kedai kopi' in x)]

    return df

def get_data_resto(df_process):
    # C1 = jumlah_review column with number if 10 reviews = 1, 100+ reviews = 2, 101-500 reviews = 3, 5001-1000 reviews = 4, 1000+ reviews = 5
    # C2 = average_price column
    # C3 = rating column with round up to nearest integer
    # C4 = set 3 
    # C5 = distance column if distance < 5km = 1, 5km-10km = 3, >10km = 5
    df_process['jumlah_review'] = df_process['jumlah_review'].apply(lambda x: 1 if x <= 10 else (2 if x <= 100 else (3 if x <= 500 else (4 if x <= 1000 else 5))))
    df_process['average_price'] = df_process['average_price']
    df_process['rating'] = df_process['rating'].apply(lambda x: round(float(x)))
    df_process['restoran_type'] = df_process['type_resto']
    df_process['distance'] = df_process.apply(lambda x: calculate_distance(lat, long, x['latitude'], x['longitude']), axis=1)
    df_process['distance'] = df_process['distance'].apply(lambda x: 1 if x <= 5 else (3 if x <= 10 else 5))
    df_process['weighted_product'] = df_process.apply(lambda x: weighted_product(x['jumlah_review'], x['average_price'], x['rating'], x['restoran_type'], x['distance']), axis=1)
    df_process = df_process.sort_values(by=['weighted_product'], ascending=False)
  
    return df_process

# pre_df = preprocessing(df)
# x_df = filter(pre_df)
# df_recommended = get_data_resto(x_df)
# print(x_df)