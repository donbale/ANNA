
from typing import Any, Dict, List, Text, Union, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
    FollowupAction,
)

class ActionGreetUser(Action):
    """Greets the user with/without privacy policy"""

    def name(self) -> Text:
        return "action_greet_user"

    def run(self, dispatcher, tracker, domain) -> List[EventType]:
        intent = tracker.latest_message["intent"].get("name")
        shown_privacy = tracker.get_slot("shown_privacy")
        name_entity = next(tracker.get_latest_entity_values("name"), None)
        if intent == "greet" or (intent == "enter_data" and name_entity):
            if shown_privacy and name_entity and name_entity.lower() != "sara":
                dispatcher.utter_message(template="utter_greet_name", name=name_entity)
                return []
            elif shown_privacy:
                dispatcher.utter_message(template="utter_greet_noname")
                return []
            else:
                dispatcher.utter_message(template="utter_greet")
                dispatcher.utter_message(template="utter_inform_privacypolicy")
                dispatcher.utter_message(template="utter_ask_goal")
                return [SlotSet("shown_privacy", True)]
        elif intent[:-1] == "get_started_step" and not shown_privacy:
            dispatcher.utter_message(template="utter_greet")
            dispatcher.utter_message(template="utter_inform_privacypolicy")
            dispatcher.utter_message(template=f"utter_{intent}")
            return [SlotSet("shown_privacy", True), SlotSet("step", intent[-1])]
        elif intent[:-1] == "get_started_step" and shown_privacy:
            dispatcher.utter_message(template=f"utter_{intent}")
            return [SlotSet("step", intent[-1])]
        return []

class stage0_form(FormAction):
    """First example training stage"""

    def name(self) -> Text:
        return "stage0_form"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return [
            "agreement",
            "person_name",
            "date_of_birth",
            "profession",
            "gender",
            "nationality",
        ]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "agreement": [
                self.from_entity(entity="training_agreement"),
                self.from_text(intent="enter_data"),
            ],
            "person_name": [
                self.from_entity(entity="person_name"),
                self.from_text(intent="enter_data"),
            ],
            "date_of_birth": [
                self.from_text(intent=None),
            ],
            "profession": [
                self.from_text(intent=None),
            ],
            "why_profession": [
                self.from_text(intent=None),
            ],
            "gender": [
                self.from_text(intent=None),
            ],
            "nationality": [
                self.from_text(intent=None)
            ],
        }

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_message(template="utter_submit_stage0")
        return []
