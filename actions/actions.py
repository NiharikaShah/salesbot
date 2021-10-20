# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from rasa_sdk.forms import FormAction
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk.events import SlotSet
from rasa_sdk.events import AllSlotsReset
from typing import Any, Text, Dict, List
import pandas as pd
import os
import xlrd
#from excel_data_store_read import DataStore

class LeadForm(FormAction):
    """Collects sales information and adds it to the spreadsheet"""

    def name(self) -> Text:
        return "lead_form"
    @staticmethod
    def required_slots(tracker):
        return [
            "name",
            "email1"
            ]

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message("Here are the information that you provided. Do you want to save it?\nName: {0},\nMobile Number: {1},\nEmail: {2},\nOccupation: {3}".format(
        tracker.get_slot("name"),
        #tracker.get_slot("number"),
        tracker.get_slot("email1")
        #tracker.get_slot("occupation")

    ))        
        return []
    
    def DataStore(name,email1):
        if os.path.isfile("user_data.xlsx"):
            df=pd.read_excel("user_data.xlsx")
            df=df.append(pd.DataFrame([[name,email1]],
                columns=["name","email1"]))
            df.to_excel("user_data.xlsx",index=False)
        else:
            df=pd.DataFrame([[name,email1]],
            columns=["name","email1"])
            df.to_excel("user_data.xlsx",index=False)
            return []
        
        
        
class ActionSaveData(Action):
    def name(self) -> Text:
        return "action_save_data"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            #LeadForm.DataStore(tracker.get_slot("name"),
            #tracker.get_slot("number"),
            #tracker.get_slot("email1"))
            #tracker.get_slot("occupation"))
            name = tracker.get_slot("name"),
            email1 = tracker.get_slot("email1")
            if(tracker.get_slot("product") is not None):
                product = tracker.get_slot("product")

                if os.path.isfile("lead_data.csv"):
                    df=pd.read_csv("lead_data.csv")
                    df=df.append(pd.DataFrame([[name,email1,product]],
                                              columns=["name","email1","product"]))
                    df.to_csv("lead_data.csv",index=False)
                else:
                    df=pd.DataFrame([[name,email1,product]],
                                    columns=["name","email1","product"])
                    df.to_csv("lead_data.csv",index=False)
                    return[] 
                 
                    
            if(tracker.get_slot("complain") is not None):
                 complain = tracker.get_slot("complain")

                 if os.path.isfile("complain.csv"):
                    df=pd.read_csv("complain.csv")
                    df=df.append(pd.DataFrame([[name,email1,complain]],
                                          columns=["name","email1","complain"]))
                    df.to_csv("complain.csv",index=False)
                 else:
                    df=pd.DataFrame([[name,email1,complain]],
                                columns=["name","email1","complain"])
                    df.to_csv("complain.csv",index=False)
                    return[]
            #dispatcher.utter_message(text="Data Stored Successfullreturn []
        
class GetIntentName(Action):        
    def name(self) -> Text:
        return "get_product_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            #LeadForm.DataStore(tracker.get_slot("name"),
            #tracker.get_slot("number"),
            #tracker.get_slot("email1"))
            #tracker.get_slot("occupation"))
            #name = tracker.get_slot("name"),
            #email1 = tracker.get_slot("email1")    
            product = tracker.get_intent_of_latest_message()
            return [SlotSet("product", product)]
        
            #return [product]
            
    

class ActionResetAllSlots(Action):

    def name(self):
        return "action_reset_all_slots"

    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]
    

class ActionSaveDataComplain(Action):
    def name(self) -> Text:
        return "action_save_data_complain"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            #LeadForm.DataStore(tracker.get_slot("name"),
            #tracker.get_slot("number"),
            #tracker.get_slot("email1"))
            #tracker.get_slot("occupation"))
            name_complain = tracker.get_slot("name_complain"),
            complain_contact = tracker.get_slot("complain_contact")
            complain = tracker.get_slot("complain")

            if os.path.isfile("complain_data.csv"):
                df=pd.read_csv("complain_data.csv")
                df=df.append(pd.DataFrame([[name_complain,complain_contact,complain]],
                    columns=["name_complain","complain_contact","complain"]))
                df.to_csv("complain_data.csv",index=False)
            else:
                df=pd.DataFrame([[name_complain,complain_contact,complain]],
                columns=["name_complain","complain_contact","complain"])
                df.to_csv("complain_data.csv",index=False)
                return[] 
            #dispatcher.utter_message(text="Data Stored Successfullreturn []
        
class GetIntentNameComplain(Action):        
    def name(self) -> Text:
        return "get_complain_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            #LeadForm.DataStore(tracker.get_slot("name"),
            #tracker.get_slot("number"),
            #tracker.get_slot("email1"))
            #tracker.get_slot("occupation"))
            #name = tracker.get_slot("name"),
            #email1 = tracker.get_slot("email1")    
            complain = tracker.latest_message.get("text")
            return [SlotSet("complain", complain)]
        
            #return [product]
            
    
