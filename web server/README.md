# How to Run This Project

To run this project locally, use the following command. By default, the webpage is served at `http://localhost:5173`, and the API server URL is `http://127.0.0.1:8000`:

```shell
vite
```

To build this project as a Docker image, use:

```shell
docker build -t cloud_computing_chatbot_web_server:latest .
```

To run this project as a Docker image, use:

```shell
docker run -e VITE_API_SERVER_URL=<URL of API server> -t cloud_computing_chatbot_web_server:latest
```

