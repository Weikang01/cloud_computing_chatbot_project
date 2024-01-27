import re

prompt_structure = "You are a helpful student assistant. {user_prompt}\nHere is the chat history:\n{chat_history}"

user_prompt_placeholders = [
    "My name is {how_bot_calls_them}, I am a {major} student in year {year}, my pronouns are {pronouns}.",
    "I am from {country}.",
    "I call you {how_they_call_bot}.",
    "My favorite sport is {favorite_sport}.",
]


def safe_format(template, **kwargs):
    class SafeDict(dict):
        def __missing__(self, key):
            return ""  # default value for missing keys

    return template.format_map(SafeDict(**kwargs))


class PromptFactory:
    _instance = None

    def __init__(self):
        self.user_prompt_placeholder_dict = {}
        for i, placeholder in enumerate(user_prompt_placeholders):
            # extract contents of curly braces with regex
            res = re.findall(r"\{(.*?)\}", placeholder)
            for item in res:
                self.user_prompt_placeholder_dict[item] = i

    def get_calendar_api_prompt(self):
        pass

    def get_user_prompt(self, personal_data):
        prompt_set = set()
        prompt = ""
        for key, value in personal_data.items():
            if key in self.user_prompt_placeholder_dict:
                if self.user_prompt_placeholder_dict[key] not in prompt_set:
                    prompt_set.add(self.user_prompt_placeholder_dict[key])
                    prompt += safe_format(user_prompt_placeholders[self.user_prompt_placeholder_dict[key]],
                                          **personal_data)

        return prompt.strip()

    def get_prompt(self, user_data, chat_history):
        bot_name = user_data.get("how_they_call_bot", "Bot") if user_data else "Bot"
        user_name = user_data.get("how_bot_calls_them", "User") if user_data else "User"

        user_prompt = self.get_user_prompt(user_data) if user_data else ""
        chat_history = "\n".join(
            f"{bot_name if entry['sender'] == 'BOT' else user_name}: {entry['message']}" for entry in chat_history
        )
        return prompt_structure.format(user_prompt=user_prompt, chat_history=chat_history)


if __name__ == '__main__':
    pf = PromptFactory()
    res = pf.get_prompt({
        'user_name': 'John',
        'major': 'computer science',
        'year': 4,
        'how_they_call_bot': 'buddy',
        'how_bot_calls_them': 'John',
        'pronouns': 'he',
        'country': 'Canada',
        'favorite_sport': 'soccer'
    }, [
        {
            "sender": "USER",
            "message": "Hello AI!",
        }
    ])
    print(res)
