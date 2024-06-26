from flask import Flask, request, jsonify
from gevent.pywsgi import WSGIServer
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

from aisdk import AISDK

# Load environment variables
load_dotenv()

app = Flask(__name__)

sdk = AISDK()

#

@app.route('/')
def test():
    return "Hello, world from inference server!"


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json

    if 'user_id' not in data or 'chat_history' not in data or 'message' not in data or 'timestamp' not in data or 'api_key' not in data:
        return jsonify({"error": "Invalid request"})

    user_id = data['user_id']
    chat_history = data['chat_history']
    calendar_response = data['calendar_response'] if 'calendar_response' in data else None
    message = data['message']
    timestamp = data['timestamp']
    api_key = data['api_key']

    # Asynchronous processing of chat message
    # is_calendar_related_request = False
    if calendar_response is None:
        response = sdk.async_process_chat_message_without_calendar(api_key, user_id, chat_history, message, timestamp)
    else:
        # is_calendar_related_request = True
        response = sdk.async_process_chat_with_calendar(api_key, user_id, chat_history, message, timestamp,
                                                        calendar_response)

    # print("-" * 50)
    # print(data)
    # print("is_calendar_related_request: " + str(is_calendar_related_request))
    # print(response)
    return jsonify(response)


@app.route('/new_user', methods=['POST'])
def new_user():
    data = request.json
    user_id = data['user_id']
    personal_data = data['personal_data']

    # Asynchronous processing for adding a new user
    greenlet = sdk.async_add_new_user(user_id, personal_data)
    greenlet.join()  # Wait for the processing to complete

    response = greenlet.value
    # print(response)
    return jsonify(response)


def main():
    # Read server configuration from environment variables
    server_address = os.getenv('SERVER_ADDRESS', '0.0.0.0')  # Default to 127.0.0.1 if not set
    server_port = int(os.getenv('SERVER_PORT', 10299))  # Default to 10299 if not set
    http_server = WSGIServer((server_address, server_port), app)

    logging.info(f"Starting server at {server_address}:{server_port}")
    http_server.serve_forever()


if __name__ == '__main__':
    main()
