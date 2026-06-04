import json

from kafka import KafkaProducer

from app.core.config import settings


class AiKafkaProducer:

    def __init__(self):
        kafka_bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS

        print(
            f"🔌 AI Kafka Producer connecting to: {kafka_bootstrap_servers}",
            flush=True
        )

        self.producer = KafkaProducer(
            bootstrap_servers=kafka_bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send_task_generation_response(self, message: dict):
        self.producer.send('ai-task-generation-response', message)
        self.producer.flush()

    def send_duplicate_detection_response(self, message: dict):
        self.producer.send('ai-duplicate-detection-response', message)
        self.producer.flush()

    def send_semantic_duplicate_detection_response(self, message: dict):
        self.producer.send('ai-semantic-duplicate-detection-response', message)
        self.producer.flush()

    def send_task_embedding_response(self, message: dict):
        self.producer.send('ai-task-embedding-response', message)
        self.producer.flush()