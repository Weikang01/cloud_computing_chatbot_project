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

  ```json
  {
      "user_id": "yp83tx8S+ZNmf/1csl1vOA==", // encoded user id
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

  
