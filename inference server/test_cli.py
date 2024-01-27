import requests
import time

# URL of your Flask app
base_url = 'http://127.0.0.1:10299'


def test_chat():
    url = f'{base_url}/chat'
    data = {
        'user_id': 'yp83tx8S+ZNmf/1csl1vOA==',
        'chat_history': [
            {
                "sender": "USER",
                "message": "Hello AI!",
                "timestamp": time.time()
            }
        ],
        'message': 'How are you?',
        'timestamp': time.time()
    }
    response = requests.post(url, json=data)
    print('Chat Response:', response.json())


def test_new_user():
    url = f'{base_url}/new_user'
    data = {
        'user_id': 'yp83tx8S+ZNmf/1csl1vOA==',
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
    # test_new_user()
    test_chat()
