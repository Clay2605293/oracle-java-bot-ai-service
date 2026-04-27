from app.models.request_models import GenerateTasksRequest
from app.models.response_models import GenerateTasksResponse
from app.services.openai_service import generate_tasks_with_openai


class TaskGenerationService:

    def generate_tasks(self, request: GenerateTasksRequest) -> GenerateTasksResponse:
        content = "\n\n".join(
            f"[{doc.type}]\n{doc.content}" for doc in request.documents
        )
        tasks = generate_tasks_with_openai(content)
        return GenerateTasksResponse(tasks=tasks)

    def generate_tasks_from_kafka(self, request_dict: dict) -> dict:
        documents = request_dict.get("documents", [])
        content = "\n\n".join(
            f"[{doc.get('type', 'DOC')}]\n{doc.get('content', '')}"
            for doc in documents
        )
        tasks = generate_tasks_with_openai(content)
        return {
            "projectId": request_dict.get("projectId"),
            "tasks": [t.model_dump() for t in tasks]
        }