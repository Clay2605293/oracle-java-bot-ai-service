from pydantic import BaseModel
from typing import List, Optional


class GeneratedTask(BaseModel):
    titulo: str
    descripcion: str
    tiempoEstimado: Optional[float] = None


class GenerateTasksResponse(BaseModel):
    tasks: List[GeneratedTask]