# How to Run This Project

To run this project locally, use the following command. By default, the API server is served at `http://localhost:8000`, and the inference server URL is `http://127.0.0.1:10299`:

```shell
npm start
```

To build this project as a Docker image, use:

```shell
docker build -t cloud_computing_chatbot_api_server:latest .
```

To run this project as a Docker image, use:

```shell
docker run -p 8000:8000 -e INFERENCE_SERVER_URL=<URL of inference server> -t cloud_computing_chatbot_api_server:latest
```

