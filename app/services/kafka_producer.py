import json
from kafka import KafkaProducer


class AiKafkaProducer:

    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers='kafka:29092',
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