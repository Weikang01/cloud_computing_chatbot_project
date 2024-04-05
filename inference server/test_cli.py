import os

import requests
import time
from dotenv import load_dotenv
# URL of your Flask app
base_url = 'http://127.0.0.1:10299'
load_dotenv()
API_KEY = os.getenv('OPENAI_API_KEY', 'your-api-key-here')


def test_chat_with_calendar():
    url = f'{base_url}/chat'
    data = {
        'user_id': 'jamesbond',
        'chat_history': [
            {
                "sender": "Bot",
                "message": "Hello, there! How may I help you?",
                "timestamp": time.time()
            }
        ],
        'calendar_response': [
            {
                "summary": "Astronomy II",
                "description": "Course:\\r\\nGSCI-2330-WDE\\r\\n\\r\\nTerm:\\r\\n2024W\\r\\n\\r\\nFaculty Info:\\r\\nN/A\\r\\n\\r\\nInstruction Method:\\r\\nWEB\\r\\n\\r\\nNo additional scheduling information available",
                "location": "N/A",
                "start": {
                    "dateTime": "2024-01-08T00:00:00-05:00",
                    "timeZone": "America/Toronto"
                },
                "end": {
                    "dateTime": "2024-04-10T00:00:00-04:00",
                    "timeZone": "America/Toronto"
                },
            }
        ],
        'message': 'Haha, that\'s funny!',
        'timestamp': time.time(),
        'api_key': API_KEY
    }
    response = requests.post(url, json=data)
    print('Chat Response:', response.json())


def test_chat_no_calendar():
    url = f'{base_url}/chat'
    data = {
        'user_id': 'jamesbond',
        'chat_history': [
            {
                "sender": "Bot",
                "message": "Hello, there! How may I help you?",
                "timestamp": time.time()
            }
        ],
        'message': 'Haha, that\'s funny!',
        'calendar_response': {},
        'timestamp': time.time(),
        'api_key': ""
    }
    response = requests.post(url, json=data)
    print('Chat Response:', response.json())


def test_new_user():
    url = f'{base_url}/new_user'
    data = {
        'user_id': 'jamesbond',
        'personal_data': {
            'major': 'computer science',
            'year': 4,
            'how_they_call_bot': 'buddy',
            'how_bot_calls_them': 'John',
            'pronouns': 'he'
        }
    }
    response = requests.post(url, json=data)
    print('New User Response:', response.json())


if __name__ == '__main__':
    test_new_user()
    test_chat_no_calendar()
    test_chat_with_calendar()
