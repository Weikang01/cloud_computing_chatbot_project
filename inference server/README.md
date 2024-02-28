# Run and test inference server

1. install Docker on your local device([Install Docker Desktop on Windows | Docker Docs](https://docs.docker.com/desktop/install/windows-install/))

2. run Docker

3. Add OpenAI API into your environment variables

   - `OPENAI_API_KEY` : your openai api key

4. In your terminal, go to root path of `inference server`

   type `docker-compose up --build`

   this command will build the docker image for the server, as well as its dependencies and start running

5. to test the server, run `test_cli.py`