from fastapi import APIRouter
from app.models.request_models import GenerateTasksRequest
from app.models.response_models import GenerateTasksResponse
from app.services.task_generation_service import TaskGenerationService

router = APIRouter(prefix="/ai", tags=["AI"])

task_generation_service = TaskGenerationService()


@router.get("/ping")
def ping_ai():
    return {
        "message": "AI route is working"
    }


@router.post("/generate-tasks", response_model=GenerateTasksResponse)
def generate_tasks(request: GenerateTasksRequest):
    return task_generation_service.generate_tasks(request)