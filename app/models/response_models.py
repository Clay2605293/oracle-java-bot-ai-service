from pydantic import BaseModel
from typing import List


class GeneratedTask(BaseModel):
    titulo: str
    descripcion: str
    priority: str
    estimatedHours: float
    suggestedDeadlineOffsetDays: int
    source: str


class GenerateTasksResponse(BaseModel):
    tasks: List[GeneratedTask]