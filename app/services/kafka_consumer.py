import json
from kafka import KafkaConsumer

from app.services.task_generation_service import TaskGenerationService
from app.services.kafka_producer import AiKafkaProducer


class AiKafkaConsumer:

    def __init__(self):
        self.consumer = KafkaConsumer(
            'ai-task-generation-request',
            bootstrap_servers='kafka:29092',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            group_id='ai-service-group',
            enable_auto_commit=True
        )

        self.task_service = TaskGenerationService()
        self.producer = AiKafkaProducer()

    def start(self):
        print("🔥 AI Kafka Consumer started...", flush=True)

        for message in self.consumer:
            print("📩 Received message:", message.value, flush=True)

            try:
                request = message.value

                # 🧠 Generar tareas
                response = self.task_service.generate_tasks_from_kafka(request)

                print("🧠 Generated tasks:", response, flush=True)

                # 📤 Enviar respuesta a Kafka
                self.producer.send_task_generation_response(response)

                print("📤 Sent response to Kafka", flush=True)

            except Exception as e:
                print("❌ Error processing message:", str(e), flush=True)