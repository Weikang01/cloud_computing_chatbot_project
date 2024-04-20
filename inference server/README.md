# How to Run This Project

To run this project locally, first install all dependencies (ideally within a virtual environment):

Create and Activate an Anaconda Environment:

```shell
conda create -n inference_server_venv python=3.10.7
conda activate inference_server_venv
conda install pip
```

install dependencies

```shell
pip install .
```

then use following command to run it:

```shell
python ./app.py
```

To build this project as a Docker image, use:

```shell
docker build -t cloud_computing_chatbot_inference_server:latest .
```

To run this project as a Docker image, use:

```shell
docker run -p 10299:10299 -t cloud_computing_chatbot_inference_server:latest
```

