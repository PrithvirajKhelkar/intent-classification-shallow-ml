from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import mysql.connector

connection = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
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
