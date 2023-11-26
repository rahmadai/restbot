import httpx 
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# read csv file
import pandas as pd
df = pd.read_csv('db/list.csv')
# print(df.loc[df['nama_resto'] == 'Gudeg Bromo Bu Tekluk'])

# menu
# fasilitas
# jenis_restaurant
# harga -> Berapaan : range harga

# Working Hours: 
# U: Jam berapa tutupnya Cinema Bakery?
# B: Jam buka [nama_resto] adalah [working_hour]

# Lokasi Resto:
# U: Dimana ya alamat Cronica Coffee Shop?
# B: Lokasi [nama_resto] di [alamat]

# class ActionCheckRestaurantsMenu(Action):
#    def name(self) -> Text:
#       return "action_check_restaurants_menu"

#    def run(self,
#            dispatcher: CollectingDispatcher,
#            tracker: Tracker,
#            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#       menu = tracker.get_slot('restaurant_name')
#       response_message = "berikut menu restoran: " + menu

#       dispatcher.utter_message(response_message)
#       return 0

class ActionCheckRestaurantsMenu(Action):
    def name(self):
        return "action_check_restaurants_menu"

    def run(self, dispatcher, tracker, domain):
        concerts = [
            {"artist": "Foo Fighters", "reviews": 4.5},
            {"artist": "Katy Perry", "reviews": 5.0},
        ]
        description = ", ".join([c["artist"] for c in concerts])
        dispatcher.utter_message(text=f"{description}")
        return [SlotSet("concerts", concerts)]
   
class ActionCheckRestaurantsLocation(Action):
    def name(self) -> Text:
        return "action_check_restaurants_location"
    
    def run(self,
              dispatcher: CollectingDispatcher,
              tracker: Tracker,
              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        # parse restaurant_name from entity
        name = tracker.latest_message['entities'][0]['value']

        # parse alamat from csv when restaurant_name is matched with nama_resto column
        location = df.loc[df['nama_resto'] == name, 'alamat'].iloc[0]
        response_message = "berikut lokasi restoran " + str(name) + " : " + str(location)
    
        dispatcher.utter_message(response_message)
        return 0
    
class ActionCheckRestaurantsWorkingHours(Action):
    def name(self) -> Text:
        return "action_check_restaurants_working_hours"
    
    def run(self,
              dispatcher: CollectingDispatcher,
              tracker: Tracker,
              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        # parse restaurant_name from entity
        # parse entities restaurant_name
        name = tracker.latest_message['entities'][1]['value']
        print(name)

        # parse alamat from csv when restaurant_name is matched with nama_resto column
        working_hour = df.loc[df['nama_resto'] == name, 'working_hour'].iloc[0]
        response_message = "Jam buka " + str(name) + " adalah : " + str(working_hour)
    
        dispatcher.utter_message(response_message)
        return 0

class ActionSuggestRestaurant(Action):

    def name(self) -> Text:
        return "action_suggest_restaurant"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        async with httpx.AsyncClient() as client:
            json_data = {"data": [{"mime_type": "text/plain", "text": tracker.latest_message['text']}]}
            resp = await client.post("http://localhost:8080/search", json=json_data)
        
        dispatcher.utter_message(text="Restaurant List :")
        matches = resp.json()['data']['docs'][0]['matches']
        for m in matches[:5]:
            dispatcher.utter_message(text=f"- {m['text']}")

        return []