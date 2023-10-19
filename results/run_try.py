import pandas as pd
import json

df = pd.read_csv('design.csv')

# id,restaurant_name,location,restaurant_type,working_hour_start,working_hour_end,harga,menu,fasilitas,lat,lon,restaurant_address

working_hour_start = 8
working_hour_end = 22
harga = 150000
menu = "Fish Roll"
fasilitas = "[mushola, baby room]"
landmark = "UGM"

a = json.loads(df["harga"][0])

print(a[0])