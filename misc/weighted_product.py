import pandas as pd

# C1 = number of review -> jumlah_review
# C2 = price -> average_price
# C3 = rating -> rating
# C4 = type -> restoran_type
# C5 = distance -> calculate distance from user location to restaurant location

lat = -7.7343303
long = 110.3901716

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
    return ((lat1-lat2)**2 + (long1-long2)**2)**0.5

# print(weighted_product(4, 3, 4, 3, 1))

# read csv
global df
df = pd.read_csv('../db/list.csv')

def get_data_resto():
    global df
    # C1 = jumlah_review column with number if 10 reviews = 1, 100+ reviews = 2, 101-500 reviews = 3, 5001-1000 reviews = 4, 1000+ reviews = 5
    # C2 = average_price column
    # C3 = rating column with round up to nearest integer
    # C4 = set 3 
    # C5 = distance column if distance < 5km = 1, 5km-10km = 3, >10km = 5
    df['jumlah_review'] = df['jumlah_review'].apply(lambda x: 1 if x <= 10 else (2 if x <= 100 else (3 if x <= 500 else (4 if x <= 1000 else 5))))
    df['average_price'] = df['average_price']
    df['rating'] = df['rating'].apply(lambda x: round(float(x)))
    df['restoran_type'] = 3
    df['distance'] = df.apply(lambda x: calculate_distance(lat, long, x['latitude'], x['longitude']), axis=1)
    df['distance'] = df['distance'].apply(lambda x: 1 if x <= 5 else (3 if x <= 10 else 5))
    df['weighted_product'] = df.apply(lambda x: weighted_product(x['jumlah_review'], x['average_price'], x['rating'], x['restoran_type'], x['distance']), axis=1)
    df = df.sort_values(by=['weighted_product'], ascending=False)
  
    return df

get_data_resto()
print(df)