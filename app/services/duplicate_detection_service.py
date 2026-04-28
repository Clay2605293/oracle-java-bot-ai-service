from app.models.request_models import DuplicateDetectionRequest
from app.services.openai_service import detect_duplicate_tasks_with_openai


class DuplicateDetectionService:

    def detect_duplicates_from_kafka(self, request_dict: dict) -> dict:
        try:
            request = DuplicateDetectionRequest(**request_dict)

            print(
                f"🔁 Starting duplicate detection for project {request.projectId} "
                f"with {len(request.tasks)} tasks",
                flush=True
            )

            if len(request.tasks) < 2:
                return {
                    "runId": request.runId,
                    "projectId": request.projectId,
                    "status": "COMPLETED",
                    "errorMessage": None,
                    "duplicates": []
                }

            tasks_as_dicts = [
                task.model_dump()
                for task in request.tasks
            ]

            duplicates = detect_duplicate_tasks_with_openai(
                tasks_as_dicts,
                request.threshold
            )

            return {
                "runId": request.runId,
                "projectId": request.projectId,
                "status": "COMPLETED",
                "errorMessage": None,
                "duplicates": [
                    duplicate.model_dump()
                    for duplicate in duplicates
                ]
            }

        except Exception as e:
            print(f"❌ Duplicate detection failed: {e}", flush=True)

            return {
                "runId": request_dict.get("runId"),
                "projectId": request_dict.get("projectId"),
                "status": "FAILED",
                "errorMessage": str(e),
                "duplicates": []
            }