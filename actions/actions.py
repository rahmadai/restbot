import httpx 
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from actions.weighted_product import preprocessing, get_data_resto

# read csv file
import pandas as pd
df = pd.read_csv('db/list.csv')
df = preprocessing(df)
df = df.assign(category=df['category'].str.split(',')).explode('category')
df = df.assign(facility=df['facility'].str.split(',')).explode('facility')

class ActionCheckRestaurantsRecommendation(Action):
    def name(self) -> Text:
        return "action_check_restaurants_recommendation"
    def run(self,
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tracker_list = tracker.latest_message['entities']
        parsed_entities = {}

        for entity_info in tracker_list:
            entity = entity_info['entity']
            value = entity_info['value']
            parsed_entities[entity] = value

        try:
            restaurant_type = parsed_entities['restaurant_type']
        except:
            restaurant_type = None
        try:
            location = parsed_entities['location']
        except:
            location = None
        try:
            restaurant_facility = parsed_entities['restaurant_facility']
        except:
            restaurant_facility = None

        # switch by combination restaurant_type, location, restaurant_facility
        if restaurant_type != None and restaurant_facility != None and location != None:
            # check in df if restaurant_type exist
            # df_exist = df[df['category'].apply(lambda x: str(restaurant_type) in x)]
            # if df_exist is not None:
            #     df_recommended = df[(df['category'].apply(lambda x: str(restaurant_type) == x)) & (df['facility'].apply(lambda x: str(restaurant_facility) == x))]
            # else:
            #     df_recommended = df[(df['facility'].apply(lambda x: str(restaurant_facility) == x))]
            df_recommended = df[(df['category'].apply(lambda x: str(restaurant_type) == x)) & (df['facility'].apply(lambda x: str(restaurant_facility) == x))]
            # limit df_recommended to 5
            df_recommended = get_data_resto(df_recommended)
            # drop duplicate by retaurant_name
            df_recommended = df_recommended.drop_duplicates(subset=['retaurant_name'])
            df_recommended = df_recommended.head(5)
            print(df_recommended)
            list_restaurant = df_recommended['retaurant_name'].tolist()
            list_restaurant = ', '.join([str(elem) for elem in list_restaurant])
            response_message = "Berikut rekomendasi " + str(restaurant_type) + " yang memiliki fasilitas : " + str(restaurant_facility) + " dan berada di sekitar lokasi : " + str(location) + " : " + str(list_restaurant)
        elif restaurant_type != None and restaurant_facility == None and location != None:
            df_recommended = df[(df['category'].apply(lambda x: str(restaurant_type) == x))]
            # limit df_recommended to 5
            df_recommended = get_data_resto(df_recommended)
            # drop duplicate by retaurant_name
            df_recommended = df_recommended.drop_duplicates(subset=['retaurant_name'])
            df_recommended = df_recommended.head(5)
            print(df_recommended)
            list_restaurant = df_recommended['retaurant_name'].tolist()
            list_restaurant = ', '.join([str(elem) for elem in list_restaurant])
            response_message = "Berikut rekomendasi " + str(restaurant_type) + " dan berada di sekitar lokasi : " + str(location) + " : " + str(list_restaurant)
        elif restaurant_type == None and restaurant_facility != None and location != None:
            df_recommended = df[(df['facility'].apply(lambda x: str(restaurant_facility) == x))]
            # limit df_recommended to 5
            df_recommended = get_data_resto(df_recommended)
            # drop duplicate by retaurant_name
            df_recommended = df_recommended.drop_duplicates(subset=['retaurant_name'])
            df_recommended = df_recommended.head(5)
            print(df_recommended)
            list_restaurant = df_recommended['retaurant_name'].tolist()
            list_restaurant = ', '.join([str(elem) for elem in list_restaurant])
            response_message = "Berikut rekomendasi restoran yang memiliki fasilitas : " + str(restaurant_facility) + " dan berada di sekitar lokasi : " + str(location) + " : " + str(list_restaurant)
        elif restaurant_type != None and restaurant_facility != None and location == None:
            df_recommended = df[(df['category'].apply(lambda x: str(restaurant_type) == x)) & (df['facility'].apply(lambda x: str(restaurant_facility) == x))]
            # limit df_recommended to 5
            df_recommended = get_data_resto(df_recommended)
            # drop duplicate by retaurant_name
            df_recommended = df_recommended.drop_duplicates(subset=['retaurant_name'])
            df_recommended = df_recommended.head(5)
            print(df_recommended)
            list_restaurant = df_recommended['retaurant_name'].tolist()
            list_restaurant = ', '.join([str(elem) for elem in list_restaurant])
            response_message = "Berikut rekomendasi " + str(restaurant_type) + " yang memiliki fasilitas : " + str(restaurant_facility) + " : " + str(list_restaurant)
        elif restaurant_type != None and restaurant_facility == None and location == None:
            df_recommended = df[(df['category'].apply(lambda x: str(restaurant_type) == x))]
            # limit df_recommended to 5
            df_recommended = get_data_resto(df_recommended)
            # drop duplicate by retaurant_name
            df_recommended = df_recommended.drop_duplicates(subset=['retaurant_name'])
            df_recommended = df_recommended.head(5)
            print(df_recommended)
            list_restaurant = df_recommended['retaurant_name'].tolist()
            list_restaurant = ', '.join([str(elem) for elem in list_restaurant])
            response_message = "Berikut rekomendasi " + str(restaurant_type) + " : " + str(list_restaurant)
        elif restaurant_type == None and restaurant_facility != None and location == None:
            df_recommended = df[(df['facility'].apply(lambda x: str(restaurant_facility) == x))]
            # limit df_recommended to 5
            df_recommended = get_data_resto(df_recommended)
            # drop duplicate by retaurant_name
            df_recommended = df_recommended.drop_duplicates(subset=['retaurant_name'])
            df_recommended = df_recommended.head(5)
            print(df_recommended)
            list_restaurant = df_recommended['retaurant_name'].tolist()
            list_restaurant = ', '.join([str(elem) for elem in list_restaurant])
            response_message = "Berikut rekomendasi restoran yang memiliki fasilitas : " + str(restaurant_facility) + " : " + str(list_restaurant)
        print(response_message)

        dispatcher.utter_message(response_message)
        return []
    
class ActionCheckRestaurantsLocation(Action):
    def name(self) -> Text:
        return "action_check_restaurants_location"
    
    def run(self,
              dispatcher: CollectingDispatcher,
              tracker: Tracker,
              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        # parse restaurant_name from entity
        name = tracker.latest_message['entities'][0]['value']
        name_lower = name.lower()
        print(name)

        # parse address from csv when restaurant_name is matched with retaurant_name column
        try:
            location = df.loc[df['retaurant_name'] == name_lower, 'address'].iloc[0]
            response_message = "berikut lokasi restoran " + str(name) + " : " + str(location)
        except:
            response_message = "Maaf, tidak ada restoran yang bernama " + str(name) + " tidak ada di database kami"

        dispatcher.utter_message(response_message)
        return []
    
class ActionCheckRestaurantsWorkingHours(Action):
    def name(self) -> Text:
        return "action_check_restaurants_working_hours"
    
    def run(self,
              dispatcher: CollectingDispatcher,
              tracker: Tracker,
              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        name = tracker.latest_message['entities'][0]['value']
        name_lower = name.lower()
        print(name)
        
        # parse address from csv when restaurant_name is matched with retaurant_name column
        try:
            working_hour = df.loc[df['retaurant_name'] == name_lower, 'working_hour'].iloc[0]
            response_message = "Jam buka " + str(name) + " adalah : " + str(working_hour)
        except:
            response_message = "Maaf, tidak ada restoran yang bernama " + str(name) + " tidak ada di database kami"
    
        dispatcher.utter_message(response_message)
        return []
    
class ActionCheckRestaurantsPricing(Action):
    def name(self) -> Text:
        return "action_check_restaurants_pricing"
    
    def run(self,
              dispatcher: CollectingDispatcher,
              tracker: Tracker,
              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        name = tracker.latest_message['entities'][0]['value']
        name_lower = name.lower()
        print(name)
        
        # parse address from csv when restaurant_name is matched with retaurant_name column
        try:
            price_ranges = df.loc[df['retaurant_name'] == name_lower, 'price_ranges'].iloc[0]
            response_message = "Range harga " + str(name) + " adalah : " + str(price_ranges)
        except:
            response_message = "Maaf, tidak ada restoran yang bernama " + str(name) + " tidak ada di database kami"
    
        dispatcher.utter_message(response_message)
        return []
    
class ActionCheckRestaurantsFacilities(Action):
    def name(self) -> Text:
        return "action_check_restaurants_facilities"
    def run(self,
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        name = tracker.latest_message['entities'][0]['value']
        name_lower = name.lower()
        print(name)

        # parse address from csv when restaurant_name is matched with retaurant_name column
        try:
            facilities = df.loc[df['retaurant_name'] == name_lower, 'facility'].iloc[0]
            response_message = "berikut fasilitas restoran " + str(name) + " : " + str(facilities)
        except:
            response_message = "Maaf, tidak ada restoran yang bernama " + str(name) + " tidak ada di database kami"
    
        dispatcher.utter_message(response_message)
        return []
    
class ActionCheckRestaurantsCategories(Action):
    def name(self) -> Text:
        return "action_check_restaurants_categories"
    def run(self,
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        category = tracker.latest_message['entities'][0]['value']
        category_lower = category.lower()
        print(category)

        # parse address from csv when restaurant_name is matched with retaurant_name column
        try:
            # get all retaurant_name with category
            # list_restaurant = df.loc[df['category'] == category, 'retaurant_name'].tolist()
            # df_recommended = df[df['category'].apply(lambda x: str(category) in x)]
            df_recommended = df[df['category'].apply(lambda x: str(category_lower) == x)]
            df_recommended = get_data_resto(df_recommended)
            print(df_recommended)
            # get retaurant_name from df_recommended
            list_restaurant = df_recommended['retaurant_name'].tolist()
            # clean list from bracket
            list_restaurant = ', '.join([str(elem) for elem in list_restaurant])
            response_message = "berikut list restoran dengan kategori " + str(category) + " : " + str(list_restaurant)
        except:
            response_message = "Maaf, tidak ada kategori " + str(category) + " tidak ada di database kami"
    
        dispatcher.utter_message(response_message)
        return []