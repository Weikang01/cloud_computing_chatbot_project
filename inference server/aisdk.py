from gevent import monkey, Greenlet
import time
import openai
import os
from dotenv import load_dotenv
import pymongo

from prompt_factory import PromptFactory

DEBUG = False
MODEL = "gpt-3.5-turbo"

# Load environment variables from .env file
load_dotenv()

# Patches standard Python sockets to be non-blocking
monkey.patch_all()


class AISDK:
    def __init__(self):
        # Initialize with any required parameters
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.llm_client = openai.OpenAI()
        self.prompt_factory = PromptFactory()

        host = os.getenv("MONGO_HOST")
        port = int(os.getenv("MONGO_PORT"))
        self.mongo_client = pymongo.MongoClient(host=host, port=port)
        self.user_db = self.mongo_client["user_db"]
        self.user_collection = self.user_db["user_collection"]

    def close(self):
        self.mongo_client.close()

    def get_user_data(self, user_id):
        return self.user_collection.find_one({"_id": user_id})

    def process_chat_without_calendar(self, user_id, chat_history, message, timestamp):
        # Start timing
        start_time = time.time()
        # Fetch user data
        user_data = self.get_user_data(user_id)

        if user_data is None:
            return {"error": "User does not exist"}

        classification = self.prompt_factory.get_input_classification_prompt(user_data['personal_data'], chat_history,
                                                                             message)

        response = self.llm_client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": classification}
            ]
        ).choices[0].message.content
        response = self.prompt_factory.clean_json_response(response)
        response["user_id"] = user_id
        response["processing_time"] = time.time() - start_time
        response["model"] = MODEL

        return response

    def process_chat_with_calendar(self, user_id, chat_history, message, timestamp, calendar_response):
        # Start timing
        start_time = time.time()
        # Fetch user data
        user_data = self.get_user_data(user_id)

        if user_data is None:
            return {"error": "User does not exist"}

        pass

    def add_new_user(self, user_id, personal_data):
        try:
            user = self.user_collection.find_one({"_id": user_id})
            if user:
                return {"error": "User already exists"}

            self.user_collection.insert_one({
                "_id": user_id,
                "personal_data": personal_data
            })
            return {
                "user_id": user_id,
                "personal_data": personal_data
            }
        except Exception as e:
            return {"error": "Database unavailable"}

    def async_process_chat_message(self, *args, **kwargs):
        if "calendar_response" in kwargs:
            return Greenlet.spawn(self.process_chat_with_calendar, *args, **kwargs)
        else:
            if len(args) == 5:
                user_id, chat_history, message, timestamp, calendar_response = args
            return Greenlet.spawn(self.process_chat_without_calendar, *args, **kwargs)

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
