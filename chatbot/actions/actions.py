from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import mysql.connector
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pass@123",
    database="student"
)

class OrderStudentCard(Action):

    def name(self) -> Text:
        return "action_order_student_card"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        student_id = next(tracker.get_latest_entity_values("student_id"), None)

        cursor = connection.cursor()

        query = "SELECT * FROM STUDENT WHERE id = %s"

        cursor.execute(query, (student_id, ))

        if cursor.fetchone():
            dispatcher.utter_template("utter_student_card_ordered", tracker)
        else:
            dispatcher.utter_template("utter_student_id_not_found", tracker)
        cursor.close()
        return []
    
class ReportCovid(Action):

    def name(self) -> Text:
        return "action_report_covid"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        student_id = tracker.get_slot("student_id")
        covid_test_type = tracker.get_slot("covid_test_type")
        covid_test_status = tracker.get_slot("covid_test_status")


        cursor = connection.cursor()

        query = "SELECT * FROM STUDENT WHERE id = %s"

        cursor.execute(query, (student_id,))

        if cursor.fetchone():
            query = "UPDATE STUDENT SET covid_test_type='"+covid_test_type+"', covid_test_status='"+covid_test_status+"'  WHERE id = '"+student_id+"';"
            cursor.execute(query)
            dispatcher.utter_template("utter_covid_test_status", tracker)
        else:
            dispatcher.utter_template("utter_student_id_not_found", tracker)
        cursor.close()
        return []
    
class GetStudentId(Action):

    def name(self) -> Text:
        return "action_get_student_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        first_name = tracker.get_slot("first_name")
        last_name = tracker.get_slot("last_name")

        cursor = connection.cursor()

        query = "SELECT * FROM STUDENT WHERE first_name = \'"+first_name+"\' and last_name = \'"+last_name+"\';"
        print(query)
        cursor.execute(query)

        result = cursor.fetchone()

        if result:
            id = result[0]
            dispatcher.utter_template("utter_student_id", tracker, student_id = id)
        else:
            dispatcher.utter_template("utter_student_not_found", tracker)
        cursor.close()
        return [SlotSet("student_id", id)]



tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

class ActionGenerateConversation(Action):
    def name(self):
        return "action_generate_conversation"

    def run(self, dispatcher, tracker, domain):
        # Get the user's message from the tracker
        user_message = tracker.latest_message['text']

        # encode the new user input, add the eos_token and return a tensor in Pytorch
        new_user_input_ids = tokenizer.encode(user_message + tokenizer.eos_token, return_tensors='pt')

        # append the new user input tokens to the chat history
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if tracker.get_slot('chat_history_ids') else new_user_input_ids

        # Set the hyperparameters
        max_length = 1000
        temperature = 0.5
        top_k = 100
        top_p = 0.7

        # generated a response while limiting the total chat history to 1000 tokens
        chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id, temperature=temperature, top_k=top_k, top_p=top_p)

        # Decode the response and send it as a RASA message
        response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        dispatcher.utter_message(response)

        # Update the chat history in the tracker
        tracker.slots['chat_history_ids'] = chat_history_ids

        return []
