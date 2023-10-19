import pandas as pd
import json

# id,restaurant_name,location,restaurant_type,working_hour_start,working_hour_end,harga,menu,fasilitas,lat,lon,restaurant_address

# filter = location, restaurant_type, working_hour, harga, menu

# rekomendasikan restaurant jepang yang ada di jakal yang buka jam 8 malam dengan harga 100 ribu dan ada menu fish roll
# p0 -> restaurant_type
# p1 -> location
# p2 -> menu
# p3 -> harga
# p4 -> working_hour

# Define a function to filter and process the CSV file based on a menu item
def filter_and_process(file_path, restaurant_type_filter, location_filter, menu_filter, harga_filter, working_hour_filter):
    df = pd.read_csv(file_path)

    for index, row in df.iterrows():
        id = row['id']
        restaurant_name = row['restaurant_name']
        working_hour_start = int(row['working_hour_start'])
        working_hour_end = int(row['working_hour_end'])
        harga = json.loads(row['harga'])
        menu = json.loads(row['menu'])
        fasilitas = json.loads(row['fasilitas'])

        for item in menu:
            if menu_filter.lower() in item.lower():
                print(f"ID: {id}")
                # print(f"Restaurant Name: {restaurant_name}")
                # print(f"Working Hour Start: {working_hour_start}")
                # print(f"Working Hour End: {working_hour_end}")
                # print(f"Harga: {harga}")
                # print(f"Menu Item: {item}")
                # print(f"Fasilitas: {fasilitas}")
                # print("\n")


file_path = 'design.csv'
restaurant_type_filter = ""
location_filter = ""
menu_filter = "Fish Roll"
harga_filter = ""
working_hour_filter = ""
filter_and_process(file_path, restaurant_type_filter, location_filter, menu_filter, harga_filter, working_hour_filter)

# berikut rekomendasi restoran yang menjual fish roll dan buka jam 9 malam

