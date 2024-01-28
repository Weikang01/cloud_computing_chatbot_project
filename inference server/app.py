from flask import Flask, request, jsonify
from aisdk import AISDK
from gevent.pywsgi import WSGIServer
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

sdk = AISDK()


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data['user_id']
    chat_history = data['chat_history']
    calendar_response = data['calendar_response'] if 'calendar_response' in data else None
    message = data['message']
    timestamp = data['timestamp']

    # Asynchronous processing of chat message
    if calendar_response is None:
        greenlet = sdk.async_process_chat_message(user_id, chat_history, message, timestamp)
    else:
        greenlet = sdk.async_process_chat_message(user_id, chat_history, message, timestamp, calendar_response)
    greenlet.join()  # Wait for the processing to complete

    response = greenlet.value
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
    server_address = os.getenv('SERVER_ADDRESS', '127.0.0.1')  # Default to 127.0.0.1 if not set
    server_port = int(os.getenv('SERVER_PORT', 10299))  # Default to 10299 if not set

    http_server = WSGIServer((server_address, server_port), app)
    http_server.serve_forever()


if __name__ == '__main__':
    main()
