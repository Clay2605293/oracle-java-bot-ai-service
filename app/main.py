from fastapi import FastAPI
from contextlib import asynccontextmanager
import threading

from app.api.routes.health import router as health_router
from app.api.routes.ai import router as ai_router
from app.services.kafka_consumer import AiKafkaConsumer

print("🔥 MAIN.PY LOADED")
@asynccontextmanager
async def lifespan(app: FastAPI):

    # 🔥 ARRANCA CONSUMER
    consumer = AiKafkaConsumer()

    def run_consumer():
        consumer.start()

    thread = threading.Thread(target=run_consumer)
    thread.daemon = True
    thread.start()

    print("🚀 AI Service started with Kafka consumer")

    yield

    print("🛑 Shutting down AI Service")


app = FastAPI(
    title="Oracle Java Bot AI Service",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(health_router)
app.include_router(ai_router)