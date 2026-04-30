import json
from kafka import KafkaConsumer

from app.services.task_generation_service import TaskGenerationService
from app.services.duplicate_detection_service import DuplicateDetectionService
from app.services.semantic_duplicate_detection_service import SemanticDuplicateDetectionService
from app.services.task_embedding_service import TaskEmbeddingService
from app.services.kafka_producer import AiKafkaProducer


class AiKafkaConsumer:

    def __init__(self):
        self.consumer = KafkaConsumer(
            'ai-task-generation-request',
            'ai-duplicate-detection-request',
            'ai-semantic-duplicate-detection-request',
            'ai-task-embedding-request',
            bootstrap_servers='kafka:29092',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            group_id='ai-service-group',
            enable_auto_commit=True
        )

        self.task_service = TaskGenerationService()
        self.duplicate_detection_service = DuplicateDetectionService()
        self.semantic_duplicate_detection_service = SemanticDuplicateDetectionService()
        self.task_embedding_service = TaskEmbeddingService()
        self.producer = AiKafkaProducer()

    def start(self):
        print("🔥 AI Kafka Consumer started...", flush=True)
        print(
            "👂 Listening topics: "
            "ai-task-generation-request, "
            "ai-duplicate-detection-request, "
            "ai-semantic-duplicate-detection-request, "
            "ai-task-embedding-request",
            flush=True
        )

        for message in self.consumer:
            print("📩 Received message from topic:", message.topic, flush=True)
            print("📩 Payload:", message.value, flush=True)

            try:
                request = message.value

                if message.topic == "ai-task-generation-request":
                    self.handle_task_generation_request(request)

                elif message.topic == "ai-duplicate-detection-request":
                    self.handle_duplicate_detection_request(request)

                elif message.topic == "ai-semantic-duplicate-detection-request":
                    self.handle_semantic_duplicate_detection_request(request)

                elif message.topic == "ai-task-embedding-request":
                    self.handle_task_embedding_request(request)

                else:
                    print(f"⚠️ Unknown topic ignored: {message.topic}", flush=True)

            except Exception as e:
                print("❌ Error processing message:", str(e), flush=True)

    def handle_task_generation_request(self, request: dict):
        response = self.task_service.generate_tasks_from_kafka(request)

        print("🧠 Generated tasks:", response, flush=True)

        self.producer.send_task_generation_response(response)

        print("📤 Sent task generation response to Kafka", flush=True)

    def handle_duplicate_detection_request(self, request: dict):
        response = self.duplicate_detection_service.detect_duplicates_from_kafka(request)

        print("🔁 Duplicate detection response:", response, flush=True)

        self.producer.send_duplicate_detection_response(response)

        print("📤 Sent duplicate detection response to Kafka", flush=True)

    def handle_semantic_duplicate_detection_request(self, request: dict):
        response = self.semantic_duplicate_detection_service.detect_semantic_duplicates_from_kafka(request)

        print("🧠 Semantic duplicate detection response:", response, flush=True)

        self.producer.send_semantic_duplicate_detection_response(response)

        print("📤 Sent semantic duplicate detection response to Kafka", flush=True)

    def handle_task_embedding_request(self, request: dict):
        response = self.task_embedding_service.generate_task_embedding_from_kafka(request)

        print("🧬 Task embedding response:", response, flush=True)

        self.producer.send_task_embedding_response(response)

        print("📤 Sent task embedding response to Kafka", flush=True)