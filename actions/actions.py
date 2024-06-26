import httpx 
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from actions.weighted_product import preprocessing, get_data_resto
from rasa_sdk.types import DomainDict

# read csv file
import pandas as pd

df = pd.read_csv('db/list.csv')
df_location = pd.read_csv('db/location_dataset.csv')
menu_df = pd.read_csv('db/menu.csv')
menu_df['restaurant_name_lower'] = menu_df['nama_resto'].str.lower()
# lowercase df_location
df_location['location_name'] = df_location['location_name'].apply(lambda x: x.lower())
df = preprocessing(df)
df = df.assign(category=df['category'].str.split(',')).explode('category')
df = df.assign(facility=df['facility'].str.split(',')).explode('facility')

df = df.merge(menu_df, on='restaurant_name_lower', how='left', indicator=True)

class ValidateRestaurantForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_restaurant_form"

    def validate_restaurant_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `restaurant_name` value."""

        # dispatcher.utter_message(text=f"OK! You want to have a {slot_value} restaurant name.")
        return {"restaurant_name": slot_value}

class ActionHandleRequests(Action):
    def name(self) -> Text:
        return "action_handle_requests"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            slot_value = tracker.get_slot('restaurant_name')
            if slot_value is None:
                return [FollowupAction("action_check_restaurants_location")]
            else:
                dispatcher.utter_message(response="utter_ask_restaurant_name")

class ActionCheckEntity(Action):
    def name(self) -> Text:
        return "action_check_entity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        requested_entity = tracker.get_slot("requested_entity")

        # You can replace 'requested_entity' with the name of the entity you're interested in
        # Check if the entity is present in the user's message
        if requested_entity:
            # Entity is present, set the slot indicating the entity is present
            return [SlotSet("entity_present", True)]
        else:
            # Entity is not present, set the slot indicating the entity is not present
            return [SlotSet("entity_present", False)]
        
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

        try:
            lat = df_location.loc[df_location['location_name'] == location, 'latitude'].iloc[0]
            long = df_location.loc[df_location['location_name'] == location, 'longitude'].iloc[0]
        except:
            lat = -7.767638
            long = 110.376639

        print(lat)
        print(long)
        # switch by combination restaurant_type, location, restaurant_facility
        try:
            if restaurant_type != None and restaurant_facility != None and location != None:
                df_recommended = df[(df['category'].apply(lambda x: str(restaurant_type) == x)) & (df['facility'].apply(lambda x: str(restaurant_facility) == x))]
                # check df_recommended is empty or not
                if df_recommended.empty:
                    response_message = "Maaf, tidak ada list restoran di database kami"
                else:
                    print(df_recommended)
                    # get latitute and longitude from df_location
                    df_recommended = get_data_resto(df_recommended, lat, long)
                    # drop duplicate by retaurant_name
                    df_recommended = df_recommended.drop_duplicates(subset=['retaurant_name'])
                    # limit df_recommended to 5
                    df_recommended = df_recommended.head(5)
                    print(df_recommended)
                    list_restaurant = df_recommended['retaurant_name'].tolist()
                    list_restaurant = ', '.join([str(elem) for elem in list_restaurant])
                    response_message = "Berikut rekomendasi " + str(restaurant_type) + " yang memiliki fasilitas : " + str(restaurant_facility) + " dan berada di sekitar lokasi : " + str(location) + " : " + str(list_restaurant)
            elif restaurant_type != None and restaurant_facility == None and location != None:
                df_recommended = df[(df['category'].apply(lambda x: str(restaurant_type) == x))]
                # check df_recommended is empty or not
                if df_recommended.empty:
                    response_message = "Maaf, tidak ada list restoran di database kami"
                else:
                    # limit df_recommended to 5
                    df_recommended = get_data_resto(df_recommended, lat, long)
                    # drop duplicate by retaurant_name
                    df_recommended = df_recommended.drop_duplicates(subset=['retaurant_name'])
                    df_recommended = df_recommended.head(5)
                    print(df_recommended)
                    list_restaurant = df_recommended['retaurant_name'].tolist()
                    list_restaurant = ', '.join([str(elem) for elem in list_restaurant])
                    response_message = "Berikut rekomendasi " + str(restaurant_type) + " dan berada di sekitar lokasi : " + str(location) + " : " + str(list_restaurant)
            elif restaurant_type == None and restaurant_facility != None and location != None:
                df_recommended = df[(df['facility'].apply(lambda x: str(restaurant_facility) == x))]
                # check df_recommended is empty or not
                if df_recommended.empty:
                    response_message = "Maaf, tidak ada list restoran di database kami"
                else:
                    # limit df_recommended to 5
                    df_recommended = get_data_resto(df_recommended, lat, long)
                    # drop duplicate by retaurant_name
                    df_recommended = df_recommended.drop_duplicates(subset=['retaurant_name'])
                    df_recommended = df_recommended.head(5)
                    print(df_recommended)
                    list_restaurant = df_recommended['retaurant_name'].tolist()
                    list_restaurant = ', '.join([str(elem) for elem in list_restaurant])
                    response_message = "Berikut rekomendasi restoran yang memiliki fasilitas : " + str(restaurant_facility) + " dan berada di sekitar lokasi : " + str(location) + " : " + str(list_restaurant)
            elif restaurant_type != None and restaurant_facility != None and location == None:
                df_recommended = df[(df['category'].apply(lambda x: str(restaurant_type) == x)) & (df['facility'].apply(lambda x: str(restaurant_facility) == x))]
                # check df_recommended is empty or not
                if df_recommended.empty:
                    response_message = "Maaf, tidak ada list restoran di database kami"
                else:
                    # limit df_recommended to 5
                    df_recommended = get_data_resto(df_recommended, lat, long)
                    # drop duplicate by retaurant_name
                    df_recommended = df_recommended.drop_duplicates(subset=['retaurant_name'])
                    df_recommended = df_recommended.head(5)
                    print(df_recommended)
                    list_restaurant = df_recommended['retaurant_name'].tolist()
                    list_restaurant = ', '.join([str(elem) for elem in list_restaurant])
                    response_message = "Berikut rekomendasi " + str(restaurant_type) + " yang memiliki fasilitas : " + str(restaurant_facility) + " : " + str(list_restaurant)
            elif restaurant_type != None and restaurant_facility == None and location == None:
                df_recommended = df[(df['category'].apply(lambda x: str(restaurant_type) == x))]
                # check df_recommended is empty or not
                if df_recommended.empty:
                    response_message = "Maaf, tidak ada list restoran di database kami"
                else:
                    # limit df_recommended to 5
                    df_recommended = get_data_resto(df_recommended, lat, long)
                    # drop duplicate by retaurant_name
                    df_recommended = df_recommended.drop_duplicates(subset=['retaurant_name'])
                    df_recommended = df_recommended.head(5)
                    print(df_recommended)
                    list_restaurant = df_recommended['retaurant_name'].tolist()
                    list_restaurant = ', '.join([str(elem) for elem in list_restaurant])
                    response_message = "Berikut rekomendasi " + str(restaurant_type) + " : " + str(list_restaurant)
            elif restaurant_type == None and restaurant_facility != None and location == None:
                df_recommended = df[(df['facility'].apply(lambda x: str(restaurant_facility) == x))]
                # check df_recommended is empty or not
                if df_recommended.empty:
                    response_message = "Maaf, tidak ada list restoran di database kami"
                else:
                    # limit df_recommended to 5
                    df_recommended = get_data_resto(df_recommended, lat, long)
                    # drop duplicate by retaurant_name
                    df_recommended = df_recommended.drop_duplicates(subset=['retaurant_name'])
                    df_recommended = df_recommended.head(5)
                    print(df_recommended)
                    list_restaurant = df_recommended['retaurant_name'].tolist()
                    list_restaurant = ', '.join([str(elem) for elem in list_restaurant])
                    response_message = "Berikut rekomendasi restoran yang memiliki fasilitas : " + str(restaurant_facility) + " : " + str(list_restaurant)
            elif restaurant_type == None and restaurant_facility == None and location != None:
                df_recommended = df
                # check df_recommended is empty or not
                if df_recommended.empty:
                    response_message = "Maaf, tidak ada list restoran di database kami"
                else:
                    # limit df_recommended to 5
                    df_recommended = get_data_resto(df_recommended, lat, long)
                    # drop duplicate by retaurant_name
                    df_recommended = df_recommended.drop_duplicates(subset=['retaurant_name'])
                    df_recommended = df_recommended.head(5)
                    print(df_recommended)
                    list_restaurant = df_recommended['retaurant_name'].tolist()
                    list_restaurant = ', '.join([str(elem) for elem in list_restaurant])
                    response_message = "Berikut rekomendasi restoran di sekitar lokasi : " + str(location) + " : " + str(list_restaurant)
            else:
                response_message = "Minta tolong untuk ulangi pertanyaan anda yang lebih spesifik?"
        except:
            response_message = "Minta tolong untuk ulangi pertanyaan anda yang lebih spesifik?"
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
        tracker_list = tracker.latest_message['entities']
        parsed_entities = {}

        for entity_info in tracker_list:
            entity = entity_info['entity']
            value = entity_info['value']
            parsed_entities[entity] = value

        try:
            name = parsed_entities['restaurant_name']
        except:
            name = None
        
        if name != None:
            # parse address from csv when restaurant_name is matched with retaurant_name column
            try:
                location = df.loc[df['restaurant_name_lower'] == name, 'address'].iloc[0]
                response_message = "berikut lokasi restoran " + str(name) + " : " + str(location)
            except:
                response_message = "Maaf, tidak ada restoran yang bernama " + str(name) + " tidak ada di database kami"
        else:
            response_message = "Maaf, tidak ada restoran tersebut di database kami"

        dispatcher.utter_message(response_message)
        return []
    
class ActionAsk24HRestaurant(Action):
    def name(self) -> Text:
        return "action_check_24h_restaurant"
    
    def run(self,
              dispatcher: CollectingDispatcher,
              tracker: Tracker,
              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        # parse restaurant_name from entity
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
        
        if restaurant_type != None:
            try:
                df_recommended = df[(df['category'].apply(lambda x: str(restaurant_type) == x))]
                # filter by column 24/7 == "yes"
                df_recommended = df_recommended[df_recommended['24/7'] == "yes"]
                # check df_recommended is empty or not
                if df_recommended.empty:
                    response_message = "Maaf, tidak ada list restoran di database kami"
                else:
                    # limit df_recommended to 5
                    # drop duplicate by retaurant_name
                    df_recommended = df_recommended.drop_duplicates(subset=['retaurant_name'])
                    df_recommended = df_recommended.head(5)
                    print(df_recommended)
                    list_restaurant = df_recommended['retaurant_name'].tolist()
                    list_restaurant = ', '.join([str(elem) for elem in list_restaurant])
                    response_message = "Berikut " + str(restaurant_type) + "yang buka 24 jam : " + str(list_restaurant)
            except:
                response_message = "Maaf, tidak ada restoran yang bernama " + str(restaurant_type) + " tidak ada di database kami"
        else:
            response_message = "Maaf, tidak ada restoran tersebut di database kami hehhee"

        dispatcher.utter_message(response_message)
        return []
    
class ActionReserveRestaurant(Action):
    def name(self) -> Text:
        return "action_reserve_restaurant"
    
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
            name = parsed_entities['restaurant_name']
        except:
            name = None

        if name != None:
            # parse address from csv when restaurant_name is matched with retaurant_name column
            try:
                number = df.loc[df['restaurant_name_lower'] == name, 'Phones'].iloc[0]
                # if number nan
                if pd.isna(number):
                    response_message = "Mohon maaf, restoran " + str(name) + " tersebut tidak memiliki kontak untuk dihubungi"
                else:
                    response_message = "Kamu bisa menghubungi " + str(name) + " di nomor berikut : " + str(number)
            except:
                response_message = "Maaf, tidak ada restoran yang bernama " + str(name) + " tidak ada di database kami"
        else:
            response_message = "Maaf, tidak ada restoran tersebut di database kami"
    
        dispatcher.utter_message(response_message)
        return []
    
class ActionCheckRestaurantDiscount(Action):
    def name(self) -> Text:
        return "action_check_restaurants_discount"
    
    def run(self,
              dispatcher: CollectingDispatcher,
              tracker: Tracker,
              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        try:
            response_message = "Mohon maaf, Restbot belum memiliki data restoran seperti yang kamu inginkan. Namun Restbot memiliki banyak rekomendasi restoran/kuliner untukmu. Apakah kamu memiliki permintaan lainnya?"
        except:
            response_message = "Mohon maaf, Restbot belum memiliki data restoran seperti yang kamu inginkan. Namun Restbot memiliki banyak rekomendasi restoran/kuliner untukmu. Apakah kamu memiliki permintaan lainnya?"

        dispatcher.utter_message(response_message)
        return []
    
class ActionCheckRestaurantsWorkingHours(Action):
    def name(self) -> Text:
        return "action_check_restaurants_working_hours"
    
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
            name = parsed_entities['restaurant_name']
        except:
            name = None

        if name != None:
            # parse address from csv when restaurant_name is matched with retaurant_name column
            try:
                working_hour = df.loc[df['restaurant_name_lower'] == name, 'working_hour'].iloc[0]
                response_message = "Jam buka " + str(name) + " adalah : " + str(working_hour)
            except:
                response_message = "Maaf, tidak ada restoran yang bernama " + str(name) + " tidak ada di database kami"
        else:
            response_message = "Maaf, tidak ada restoran tersebut di database kami"
    
        dispatcher.utter_message(response_message)
        return []
    
class ActionEntityKosong(Action):
    def name(self) -> Text:
        return "action_entity_kosong"
    
    def run(self,
              dispatcher: CollectingDispatcher,
              tracker: Tracker,
              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        response_message = "Contoh entity kosong"
    
        dispatcher.utter_message(response_message)
        return []
    
class ActionCheckRestaurantsPricing(Action):
    def name(self) -> Text:
        return "action_check_restaurants_pricing"
    
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
            name = parsed_entities['restaurant_name']
        except:
            name = None
        
        if name != None:
            # parse address from csv when restaurant_name is matched with retaurant_name column
            try:
                # retrieve menu and rank_menu from menu_df while restaurant_name_lower == name
                menu = df.loc[df['restaurant_name_lower'] == name, ['menu', 'harga']]
                # get distict value from menu and rank_menu
                menu = menu.drop_duplicates(subset=['menu', 'harga'])
                # order by rank_menu ascending
                menu = menu.sort_values(by=['harga'], ascending=True)

                if menu.empty:
                    response_message = "Maaf, tidak ada restoran yang bernama " + str(name) + " tidak ada di database kami"
                # retrieve only column menu and top 2
                # menu = menu['menu'].head(2).tolist()
                else:
                    response_message = "berikut list harga dari restoran " + str(name) + " : " + str(menu)
            except:
                response_message = "Maaf, tidak ada restoran yang bernama " + str(name) + " tidak ada di database kami"
        else:
            response_message = "Maaf, tidak ada restoran tersebut di database kami"
    
        dispatcher.utter_message(response_message)
        return []
    
class ActionCheckRestaurantsFacilities(Action):
    def name(self) -> Text:
        return "action_check_restaurants_facilities"
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
            name = parsed_entities['restaurant_name']
        except:
            name = None

        if name != None:
            # parse address from csv when restaurant_name is matched with retaurant_name column
            try:
                facilities = df.loc[df['restaurant_name_lower'] == name, 'facility']
                # drop duplicate by facility
                facilities = facilities.drop_duplicates()
                # get list of facilities
                facilities = facilities.tolist()
                response_message = "berikut fasilitas restoran " + str(name) + " : " + str(facilities)
            except:
                response_message = "Maaf, tidak ada restoran yang bernama " + str(name) + " tidak ada di database kami"
        else:
            response_message = "Maaf, tidak ada restoran tersebut di database kami"
    
        dispatcher.utter_message(response_message)
        return []
    
class ActionCheckRestaurantsMenu(Action):
    def name(self) -> Text:
        return "action_check_restaurants_menu"
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
            name = parsed_entities['restaurant_name']
        except:
            name = None

        if name != None:
            # parse address from csv when restaurant_name is matched with retaurant_name column
            try:
                # retrieve menu and rank_menu from menu_df while restaurant_name_lower == name
                menu = df.loc[df['restaurant_name_lower'] == name, ['menu', 'rank_menu']]
                # get distict value from menu and rank_menu
                menu = menu.drop_duplicates(subset=['menu', 'rank_menu'])
                # order by rank_menu ascending
                menu = menu.sort_values(by=['rank_menu'], ascending=True)
                # retrieve only column menu and top 2
                menu = menu['menu'].tolist()
                response_message = "berikut list seluruh menu dari restoran " + str(name) + " : " + str(menu)
            except:
                response_message = "Maaf, tidak ada restoran yang bernama " + str(name) + " tidak ada di database kami"
        else:
            response_message = "Maaf, tidak ada restoran tersebut di database kami"
    
        dispatcher.utter_message(response_message)
        return []
    

class ActionCheckRecommendationMenuRestaurants(Action):
    def name(self) -> Text:
        return "action_check_recommendation_menu_restaurants"
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
            name = parsed_entities['restaurant_name']
        except:
            name = None

        if name != None:
            # parse address from csv when restaurant_name is matched with retaurant_name column
            try:
                # retrieve menu and rank_menu from menu_df while restaurant_name_lower == name
                menu = df.loc[df['restaurant_name_lower'] == name, ['menu', 'rank_menu']]
                # get distict value from menu and rank_menu
                menu = menu.drop_duplicates(subset=['menu', 'rank_menu'])
                # order by rank_menu ascending
                menu = menu.sort_values(by=['rank_menu'], ascending=True)
                # retrieve only column menu and top 2
                menu = menu['menu'].head(2).tolist()
                response_message = "berikut rekomendasi menu dari restoran " + str(name) + " : " + str(menu)
            except:
                response_message = "Maaf, tidak ada restoran yang bernama " + str(name) + " tidak ada di database kami"
        else:
            response_message = "Maaf, tidak ada restoran tersebut di database kami"
    
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