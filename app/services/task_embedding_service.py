import json

from openai import OpenAI

from app.core.config import settings


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


class TaskEmbeddingService:

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_task_embedding_from_kafka(self, request_dict: dict) -> dict:
        try:
            task_id = request_dict.get("taskId")
            project_id = request_dict.get("projectId")
            title = str(request_dict.get("titulo", "") or "").strip()
            description = str(request_dict.get("descripcion", "") or "").strip()
            embedding_model = request_dict.get("embeddingModel") or DEFAULT_EMBEDDING_MODEL

            if not task_id:
                raise ValueError("taskId is required")

            if not project_id:
                raise ValueError("projectId is required")

            if not title:
                raise ValueError("titulo is required")

            embedding_text = self._build_embedding_text(title, description)

            print(
                f"🧠 Generating embedding for task {task_id} using {embedding_model}",
                flush=True
            )

            response = self.client.embeddings.create(
                model=embedding_model,
                input=embedding_text
            )

            embedding = response.data[0].embedding

            return {
                "taskId": task_id,
                "projectId": project_id,
                "status": "COMPLETED",
                "errorMessage": None,
                "embeddingModel": embedding_model,
                "embeddingText": embedding_text[:1000],
                "embeddingJson": json.dumps(embedding)
            }

        except Exception as e:
            print(f"❌ Task embedding generation failed: {e}", flush=True)

            return {
                "taskId": request_dict.get("taskId"),
                "projectId": request_dict.get("projectId"),
                "status": "FAILED",
                "errorMessage": str(e),
                "embeddingModel": request_dict.get("embeddingModel") or DEFAULT_EMBEDDING_MODEL,
                "embeddingText": None,
                "embeddingJson": None
            }

    def _build_embedding_text(self, title: str, description: str) -> str:
        if description:
            return f"Título: {title}\nDescripción: {description}"

        return f"Título: {title}"
