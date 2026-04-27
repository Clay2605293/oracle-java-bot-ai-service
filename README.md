# oracle-java-bot-ai-service

## Run with Docker using .env

Create a `.env` file in the project root (you can copy from `.env.example`):

OPENAI_API_KEY=sk-proj-...

Build and run:

docker build -t oracle-java-bot-ai-service:latest .
docker rm -f oracle-java-bot-ai-service
docker run --network oracle-java-bot-backend_broker-kafka --name oracle-java-bot-ai-service -p 8090:8090 --env-file .env oracle-java-bot-ai-service:latest

