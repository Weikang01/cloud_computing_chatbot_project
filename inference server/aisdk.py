from gevent import monkey, Greenlet, joinall

monkey.patch_all()
import time
import os
from dotenv import load_dotenv
import openai

from prompt_factory import PromptFactory
from discriminator import Discriminator
import logging


# Load environment variables from .env file
load_dotenv()

DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't', 'y', 'yes')
logging.info(f"Current DEBUG status: {DEBUG}")

DEBUG_CALENDAR = True
MODEL = "gpt-3.5-turbo"
NR_RESPONSES = 1


class AISDK:
    def __init__(self):
        # Initialize with any required parameters
        self.prompt_factory = PromptFactory()
        self.disc = Discriminator(256)
        self.users = {}

        data = {
            'user_id': 'jamesbond',
            'personal_data': {
                'major': 'computer science',
                'year': 4,
                'how_they_call_bot': 'Weikang',
                'how_bot_calls_them': 'Weikang',
                'pronouns': 'he'
            }
        }

        self.add_new_user("jamesbond", data['personal_data'])

    def close(self):
        pass

    def get_user_data(self, user_id):
        return self.users.get(user_id, None)

    def request_worker(self, api_key, user_id, prompt):
        global DEBUG_CALENDAR
        # Start timing
        start_time = time.time()
        llm_client = None
        try:
            llm_client = openai.OpenAI(api_key=api_key)
            llm_client.models.list()
        except Exception as e:
            llm_client = None
            return {"error": "API key incorrect or unavailable"}
        finally:
            if llm_client is None:
                return {"error": "API key incorrect or unavailable"}

        if DEBUG:
            if DEBUG_CALENDAR:
                response = "{\"maxResults\": \"1\", \"onlyCourse\": \"true\", \"orderBy\": \"startTime\", \"timeMax\": \"\", \"timeMin\": \"2024-03-06T02:15:29.404306Z\"}"
                DEBUG_CALENDAR = False
            else:
                response = "{\"input_message\": \"Hello!\", \"response\": \"Hello, how are you?\"}"  # For testing
                DEBUG_CALENDAR = True
        else:
            try:
                response = llm_client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                ).choices[0].message.content
            except Exception as e:
                response = "{\"error\": \"OpenAI API unavailable\"}"
        response = self.prompt_factory.clean_json_response(response)

        response["user_id"] = user_id
        response["processing_time"] = time.time() - start_time
        response["model"] = MODEL
        return response

    def add_new_user(self, user_id, personal_data):
        try:
            user = self.get_user_data(user_id)
            if user:
                return {"error": "User already exists"}

            self.users[user_id] = personal_data
            return {
                "user_id": user_id,
                "personal_data": personal_data
            }
        except Exception as e:
            return {"error": "Database unavailable"}

    def async_process_chat_with_calendar(self, api_key, user_id, chat_history, message, timestamp, calendar_response,
                                         *args,
                                         **kwargs):
        # Fetch user data
        user_data = self.get_user_data(user_id)

        if user_data is None:
            return {"error": "User does not exist"}

        prompt = self.prompt_factory.get_calendar_response_prompt(user_data, chat_history, message,
                                                                  calendar_response)

        greenlets = [
            Greenlet.spawn(self.request_worker, api_key, user_id, prompt)
            for _ in range(NR_RESPONSES)
        ]

        joinall(greenlets)  # Wait for all greenlets to complete
        responses = [greenlet.value for greenlet in greenlets]

        return self.disc.pick_best_response(message, responses)

    def async_process_chat_message_without_calendar(self, api_key, user_id, chat_history, message, timestamp, *args,
                                                    **kwargs):
        # Fetch user data
        user_data = self.get_user_data(user_id)

        if user_data is None:
            return {"error": "User does not exist"}

        prompt = self.prompt_factory.get_input_classification_prompt(user_data, chat_history, message)

        greenlets = [
            Greenlet.spawn(self.request_worker, api_key, user_id, prompt)
            for _ in range(NR_RESPONSES)
        ]

        joinall(greenlets)  # Wait for all greenlets to complete
        responses = [greenlet.value for greenlet in greenlets]

        return self.disc.pick_best_response(message, responses)

    def async_add_new_user(self, *args, **kwargs):
        return Greenlet.spawn(self.add_new_user, *args, **kwargs)


# Example Usage
if __name__ == "__main__":
    sdk = AISDK()
    # Simulating async requests
    sdk.add_new_user("yp83tx8S+ZNmf/1csl1vOA==", {
        "major": "computer science",
        "year": 4,
        "how_they_call_bot": "friend",
        "how_bot_calls_them": "Tom",
        "pronouns": "he"
    })
    sdk.close()
