from pydantic import BaseModel
from typing import List, Optional


class GeneratedTask(BaseModel):
    titulo: str
    descripcion: str
    tiempoEstimado: Optional[float] = None


class GenerateTasksResponse(BaseModel):
    tasks: List[GeneratedTask]


class DuplicateCandidate(BaseModel):
    taskAId: str
    taskBId: str
    taskATitle: str
    taskBTitle: str
    similarityScore: float
    reason: Optional[str] = None


class DuplicateDetectionResponse(BaseModel):
    runId: str
    projectId: str
    status: str
    errorMessage: Optional[str] = None
    duplicates: List[DuplicateCandidate]