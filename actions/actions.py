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
df = df.assign(kategori=df['kategori'].str.split(',')).explode('kategori')

class ActionCheckRestaurantsLocation(Action):
    def name(self) -> Text:
        return "action_check_restaurants_location"
    
    def run(self,
              dispatcher: CollectingDispatcher,
              tracker: Tracker,
              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        # parse restaurant_name from entity
        name = tracker.latest_message['entities'][0]['value']
        print(name)

        # parse alamat from csv when restaurant_name is matched with nama_resto column
        try:
            location = df.loc[df['nama_resto'] == name, 'alamat'].iloc[0]
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
        print(name)
        
        # parse alamat from csv when restaurant_name is matched with nama_resto column
        try:
            working_hour = df.loc[df['nama_resto'] == name, 'working_hour'].iloc[0]
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
        print(name)
        
        # parse alamat from csv when restaurant_name is matched with nama_resto column
        try:
            working_hour = df.loc[df['nama_resto'] == name, 'working_hour'].iloc[0]
            response_message = "Jam buka " + str(name) + " adalah : " + str(working_hour)
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
        print(name)

        # parse alamat from csv when restaurant_name is matched with nama_resto column
        try:
            facilities = df.loc[df['nama_resto'] == name, 'facilities'].iloc[0]
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
        print(category)

        # parse alamat from csv when restaurant_name is matched with nama_resto column
        try:
            # get all nama_resto with category
            # list_restaurant = df.loc[df['kategori'] == category, 'nama_resto'].tolist()
            # df_recommended = df[df['kategori'].apply(lambda x: str(category) in x)]
            df_recommended = df[df['kategori'].apply(lambda x: str(category) == x)]
            df_recommended = get_data_resto(df_recommended)
            print(df_recommended)
            # get nama_resto from df_recommended
            list_restaurant = df_recommended['nama_resto'].tolist()
            # clean list from bracket
            list_restaurant = ', '.join([str(elem) for elem in list_restaurant])
            response_message = "berikut list restoran dengan kategori " + str(category) + " : " + str(list_restaurant)
        except:
            response_message = "Maaf, tidak ada kategori " + str(category) + " tidak ada di database kami"
    
        dispatcher.utter_message(response_message)
        return []