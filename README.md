# Chatbot Team Project - Cloud Computing COMP-4312



<img src="./images/project structure2.drawio.png" alt="project structure2.drawio" style="zoom:67%;" />

The project contains three main components, each of them will be deployed in a separate server on cloud, they are

1. A web-based frontend based on React.js
2. An API server based on node.js and express.js, it should also store the chat history of the user
3. An inference server based on flask and openAI's API

## Inter-server communication

We will use JSON based REST API to handle inter-server communication, here are sample API's

### API server

* `/chat` method: **POST**

  request body

  ```json
  {
      "user_id": "jamesbond",
      "message": "how are you doing?"
  }
  ```

  response format

  ```json
  {
      "user_id": "jamesbond",
      "respond": "I'm good"
  }
  ```

* `/new_user` method: **POST**

  request body

  ```json
  {
      "user_id": "jamesbond",
      "personal_data": {
          "major": "computer science",
          "year": 4,
          // add more if needed
      }
  }
  ```

  response format

  ```json
  {
      "status": true,  // true=success, false=fail
      "message": "user added"
  }
  ```

* `/chat_history` method: **POST**

  request body

  ```json
  {
      "user_id": "jamesbond"
  }
  ```

  response format

  ```json
  {
      "user_id": "jamesbond",
      "chat_history": [
          {
              "sender": "USER",
              "message": "hello world, AI!",
              "timestamp": 123134123
          },
          {
              "sender": "BOT",
              "message": "hello world, user!",
              "timestamp": 123134123
          }
      ]
  }
  ```

  

### Inference server

inference server ONLY communicates with API server

* `/chat` method: **POST**

  request body

  there are **TWO** types of request body, the first is the one **without** checking calendar data 

  ```json
  {
      "user_id": "yp83tx8S+ZNmf/1csl1vOA==", // encoded user id
      "chat_history": [
          {
              "sender": "USER",
              "message": "hello world, AI!",
              "timestamp": 123134123
          },
          {
              "sender": "BOT",
              "message": "hello world, user!",
              "timestamp": 123134123
          }
      ],
      "message": "how are you doing?",
      "timestamp": 123134123
  }
  ```

  response format

  ```json
  {
      "user_id": "yp83tx8S+ZNmf/1csl1vOA==", // encoded user id
      "respond": "I'm good"
  }
  ```

  

* `/new_user` method: **POST**

  request body

  if the model believes that the current message is a general chat, it will return the response:
  
  ```json
  {
    "input_classification": "general",
    "input_message": "John: Haha, that's funny!",
    "match_score": "80",
    "model": "gpt-3.5-turbo",
    "processing_time": 3.212432622909546,
    "response": "Hello John! I'm glad you found it funny. Is there anything specific you need help with?",
    "user_id": "yp83tx8S+ZNmf/1csl1vOA=="
  }
  
  ```
  
  in this case, API server should return the response["response"] to client as chatbot's output.
  
  If the model believes that the current message is asking for "calendar", however it will respond a set of arguments for the API server to fetch Google calendar's API.
  
  ```json
  {
  	"input_message": "Tom: Give me a calendar event for tomorrow at 10am",
  	"input_classification": "calendar",
  	"match_score": "100",
  	"response": {
  		"maxResults": "1",
  		"orderBy": "startTime",
  		"timeMin": "2024-01-28T10:00:00Z",
  		"timeMax": "2024-01-28T11:00:00Z"
  	}
  }
  ```
  
  
  
  
  
  response format
  
  ```json
  {
      "status": true,  // true=success, false=fail
      "message": "user added"
  }
  ```
  
  
