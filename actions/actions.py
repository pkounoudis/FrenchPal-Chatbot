# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []

import openai

def get_answers_from_chatgpt(user_text):

    # OpenAI API Key
    openai.api_key = ""

    # Use OpenAI API to get the response for the given user text and intent
    output = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-1106",
        messages = [{"role": "user",
                    "content": "Translate this in English: " + user_text

        }]
    )

    final_output = output["choices"][0]["message"]["content"]
    # Return the response from OpenAI
    return final_output


def get_exercises_from_chatgpt(user_text):

    # OpenAI API Key
    openai.api_key = ""

    # Use OpenAI API to get the response for the given user text and intent
    output = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-1106",
        messages = [{"role": "user",
                    "content": "Write me a small (5 questions) french vocabulary exercise (A2 level)" + user_text

        }]
    )

    final_output = output["choices"][0]["message"]["content"]
    # Return the response from OpenAI
    return final_output


class Simple_ChatGPT_Action(Action):

    """Rasa action to parse user text and pulls a corresponding answer 
    from ChatGPT."""

    def name(self) -> Text:
        return "action_show_translation" 

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the latest user text 
        user_text_for_translation = tracker.latest_message.get('text')

        if len(user_text_for_translation.split(" ")) <= 50:

            # Dispatch the response from OpenAI to the user
            trans = get_answers_from_chatgpt(user_text_for_translation)
            msg = f'Here you are! {trans}'
            dispatcher.utter_message(text=msg)
            return []

        else:
            dispatcher.utter_message(text='Your text is too big!')
            return []
        

class French_Exercises(Action):

    """Rasa action to parse user text and pulls a corresponding answer 
    from ChatGPT."""

    def name(self) -> Text:
        return "action_show_exercises" 

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        exercise_level = tracker.get_slot("ex_level")

            # OpenAI API Key
        openai.api_key = ""

        # Use OpenAI API to get the response for the given user text and intent
        output = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo-1106",
            messages = [{"role": "user",
                        "content": "Write me a small grammar french exercise with 5 subquestions" + str(exercise_level)
            }]
        )

        final_output = f'Here is some {exercise_level} exercises! {output["choices"][0]["message"]["content"]}'
        # Return the response from OpenAI

        dispatcher.utter_message(text=final_output)
        return []


verbs_db = {'parler': "Je parle, Tu parles, Il/Elle parle, Nous parlons, Vous parlez, Ils/Elles parlent",
            'finir': "Je finis (I finish), tu finis (you finish), il, elle finit (he, she finishes), nous finissons (we finish), vous finissez (you finish) and ils, elles finissent (they finish)",
            'apprendre': "j'apprends, tu apprends, il apprend, nous apprenons, vous apprenez, ils apprennent",
            'etre': "Je suis (I am), Tu es (you are, familiar), Il, elle, on est (He, she, one is), Nous sommes (We are), Vous êtes (You are) and Ils, elles sont (They are)"}


class Verb_Conjugator(Action):

    def name(self) -> Text:
        return "action_conjugate_verbs"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the latest user text 
        current_verb = tracker.latest_message.get("text")

        if str(current_verb) not in list(verbs_db.keys()):
            msg = f"{current_verb}, is either not in the list or you mispelled it!"
            dispatcher.utter_message(text=msg)
            return []
            
        msg = f"Here it is! {verbs_db[current_verb]}"
        dispatcher.utter_message(text=msg)

        return []

        # user_id = tracker.get_slot('UserID')
        # current_verb = tracker.latest_message.get('text')
