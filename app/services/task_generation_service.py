from app.models.request_models import GenerateTasksRequest
from app.models.response_models import GenerateTasksResponse
from app.services.document_service import extract_text_from_url
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
        parts = []

        for doc in documents:
            doc_type = doc.get("type", "DOC")
            url = doc.get("url")
            content = doc.get("content", "")

            if url:
                print(f"Downloading document from: {url}", flush=True)
                try:
                    content = extract_text_from_url(url)
                    print(
                        f"Extracted {len(content)} chars from {doc_type}",
                        flush=True,
                    )
                except Exception as e:
                    print(f"Failed to download {url}: {e}", flush=True)

            if content:
                parts.append(f"[{doc_type}]\n{content}")

        tasks = generate_tasks_with_openai("\n\n".join(parts))
        return {
            "projectId": request_dict.get("projectId"),
            "tasks": [t.model_dump() for t in tasks]
        }