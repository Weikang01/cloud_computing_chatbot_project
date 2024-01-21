from gevent import monkey, Greenlet
import time
import openai
import os
import json
from neo4j import GraphDatabase
from dotenv import load_dotenv
from neo4j.exceptions import ServiceUnavailable

# Load environment variables from .env file
load_dotenv()

# Patches standard Python sockets to be non-blocking
monkey.patch_all()


class AISDK:
    def __init__(self):
        # Initialize with any required parameters
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI()

        uri = os.getenv("NEO4J_URI")
        user = os.getenv("NEO4J_USER")
        password = os.getenv("NEO4J_PASSWORD")
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_user_data(self, user_id):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_user, user_id)
            return result

    @staticmethod
    def _find_user(tx, user_id):
        query = (
            "MATCH (u:User {user_id: $user_id}) "
            "RETURN u.personal_data"
        )
        result = tx.run(query, user_id=user_id)
        return result.single()[0] if result.single() else None

    def process_chat_message(self, user_id, chat_history, message, timestamp):
        # Fetch user data
        user_data = self.get_user_data(user_id)
        if user_data:
            user_data = json.loads(user_data)  # Assuming personal_data is stored as a JSON string

            bot_name = user_data.get("how_they_call_bot", "Bot")
            user_name = user_data.get("how_bot_calls_them", "User")

            system_prompt = f"You are a helpful student assistant, here are my personal data {user_data}, I call you {bot_name}, and you call me {user_name}. Here is the chat history:\n"
        else:
            bot_name = "Bot"
            user_name = "User"

            system_prompt = f"You are a helpful student assistant, I call you {bot_name}, and you call me {user_name}. Here is the chat history:\n"

        system_prompt += "\n".join(
            f"{bot_name if entry['sender'] == 'BOT' else user_name}: {entry['message']}" for entry in chat_history
        )

        # Start timing
        start_time = time.time()

        # OpenAI API call
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=100
        )

        # Return a dictionary with the relevant information
        return {
            "user_id": user_id,
            "response": response.choices[0].message.content,
            # "response": "done",
            "processing_time": time.time() - start_time,  # Actual processing time
            "model": "gpt-3.5-turbo"
        }

    def add_new_user(self, user_id, personal_data):
        with self.driver.session() as session:
            MAX_RETRY = 3
            retry = 0
            while retry < MAX_RETRY:
                try:
                    return session.write_transaction(self._create_and_return_user, user_id, personal_data)
                except ServiceUnavailable:
                    print("Database unavailable, retrying...")
                    time.sleep(1)
                    retry += 1
                    continue

            # return an error if MAX_RETRY is reached
            return {"error": "Database unavailable"}

    def _create_and_return_user(self, tx, user_id, personal_data):
        query = (
            "CREATE (u:User {user_id: $user_id, personal_data: $personal_data}) "
            "RETURN u.user_id AS user_id, u.personal_data AS personal_data"
        )
        result = tx.run(query, user_id=user_id, personal_data=json.dumps(personal_data))
        record = result.single()
        if record:
            return {
                "user_id": record["user_id"],
                "personal_data": json.loads(record["personal_data"])
            }
        else:
            return {"error": "Unable to create user"}

    def async_process_chat_message(self, *args, **kwargs):
        return Greenlet.spawn(self.process_chat_message, *args, **kwargs)

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
