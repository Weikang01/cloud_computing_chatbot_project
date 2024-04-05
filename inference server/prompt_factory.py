import datetime
import json

from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
import re

prompt_structure = "{input_classification_prompt}"

user_prompt_placeholders = [
    "My name is {how_bot_calls_them}.",
    "I am a {year} year {major} student.",
    "My pronouns are {pronouns}.",
    "I am from {country}.",
    "I call you {how_they_call_bot}.",
    "My favorite sport is {favorite_sport}.",
]

user_input_classifications = [
    "general",
    "calendar",
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

    @staticmethod
    def get_chat_history_prompt(chat_history, how_bot_calls_them="User", how_they_call_bot="Bot"):
        chat_history = "\n".join(
            f"{how_bot_calls_them if entry['sender'] == 'User' else how_they_call_bot}: {entry['message']}" for entry in
            chat_history
        )
        return chat_history

    def _get_input_classification_prompt(self, cur_message, chat_history, how_bot_calls_them="User",
                                         how_they_call_bot="Bot", user_data=None):
        user_prompt = self.get_user_prompt(user_data) if user_data else ""

        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time

        response_schemas = [
            ResponseSchema(name="input_message", description="This is the current_message from the user"),
            ResponseSchema(name="input_classification",
                           description="This is the topic you feel is most closely matched to the users current message"),
            ResponseSchema(name="match_score",
                           description="A score 0-100 of how close you think the match is between user input and your match"),
            ResponseSchema(name="response", description="You should return a response based on the following schema"),
        ]

        calendar_schemas = [
            ResponseSchema(name="maxResults",
                           description="The maximum number of events returned on one result page. Optional."),
            ResponseSchema(name="orderBy", description="The order of the events returned in the result. Optional."),
            ResponseSchema(name="timeMin",
                           description=f"Lower bound (inclusive) for an event's end time to filter by. Optional. Now is {now} by default."),
            ResponseSchema(name="timeMax",
                           description="Upper bound (exclusive) for an event's end time to filter by. Optional."),
            ResponseSchema(name="onlyCourse",
                           description="Only return events that are courses. Optional. Default is false."),
        ]

        calender_parser = StructuredOutputParser.from_response_schemas(calendar_schemas)
        calendar_format_instructions = calender_parser.get_format_instructions()

        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions()

        chat_history = PromptFactory.get_chat_history_prompt(chat_history, how_bot_calls_them, how_they_call_bot)
        template = f"""
        You are a helpful student assistant.
        {user_prompt}
        Here is a conversation between you and me.
        Find the best topic for the latest message.
        The closest match will be the one with the closest semantic meaning. Not just string similarity.
        
        {{format_instructions}}
        
        if you think the message is about the calendar, you can use the following format:
        
        {{calendar_format_instructions}}
        
        Wrap your final output with closed and open curly brackets (a JSON object).
        
        INPUT MESSAGE:
        {how_bot_calls_them}: {cur_message}
        
        CHAT HISTORY (for context):
        {chat_history}
        
        INPUT CLASSIFICATION:
        {{input_classification}}
        """

        prompt = ChatPromptTemplate(
            messages=[
                HumanMessagePromptTemplate.from_template(template)
            ],
            input_variables=["input_classification"],
            partial_variables={"format_instructions": format_instructions,
                               "calendar_format_instructions": calendar_format_instructions}
        )
        input_classification = ", ".join(user_input_classifications)
        _input = prompt.format_prompt(input_classification=input_classification)

        return _input.to_string()

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

    def get_input_classification_prompt(self, user_data, chat_history, current_message):
        bot_name = user_data.get("how_they_call_bot", "Bot") if user_data else "Bot"
        user_data["how_they_call_bot"] = bot_name
        user_name = user_data.get("how_bot_calls_them", "User") if user_data else "User"
        user_data["how_bot_calls_them"] = user_name

        return self._get_input_classification_prompt(current_message, chat_history,
                                                     how_bot_calls_them=user_name,
                                                     how_they_call_bot=bot_name,
                                                     user_data=user_data)

    def _get_calendar_response_prompt(self, calendar_response):
        """
        sample calendar_response:
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
        ]
        :param calendar_response:
        :return:
        """
        prompt = ''

        for i, event in enumerate(calendar_response):
            prompt += f"""
Event {i + 1}:
Summary: {event['summary']}
Description: {event['description']}
Location: {event['location']}
Start: {event['start']['dateTime']}
End: {event['end']['dateTime']}
"""
        return prompt

    def get_calendar_response_prompt(self, user_data, chat_history, current_message, calendar_response):
        bot_name = user_data.get("how_they_call_bot", "Bot") if user_data else "Bot"
        user_data["how_they_call_bot"] = bot_name
        user_name = user_data.get("how_bot_calls_them", "User") if user_data else "User"
        user_data["how_bot_calls_them"] = user_name

        user_prompt = self.get_user_prompt(user_data)
        chat_history = self.get_chat_history_prompt(chat_history, how_bot_calls_them=user_name,
                                                    how_they_call_bot=bot_name)
        calendar_response_prompt = self._get_calendar_response_prompt(calendar_response)
        response_schemas = [
            ResponseSchema(name="input_message", description="This is the current_message from the user"),
            ResponseSchema(name="response", description="You should return a response based on the following schema"),
        ]

        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions()

        template = f"""
You are a helpful student assistant.
{user_prompt}
Here is a conversation between you and me.
{chat_history}

Wrap your final output with closed and open curly brackets (a JSON object).

RESPONSE FORMAT:
{{format_instructions}}

INPUT MESSAGE:
{user_name}: {current_message}

RELATED CALENDAR EVENTS:
{calendar_response_prompt}

RESPONSE:"""

        prompt = ChatPromptTemplate(
            messages=[
                HumanMessagePromptTemplate.from_template(template)
            ],
            partial_variables={"format_instructions": format_instructions}
        )

        return prompt.format_prompt().to_string()

    @staticmethod
    def clean_json_response(response):
        response = response.replace("```json", "").replace("```", "").replace("\"{", "")\
            .replace("}\"", "").replace(r"\"", "").strip()
        return json.loads(response)


if __name__ == '__main__':
    pf = PromptFactory().get_input_classification_prompt("Hello AI!", [
        {
            "sender": "USER",
            "message": "Hello AI!",
        }
    ])

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
