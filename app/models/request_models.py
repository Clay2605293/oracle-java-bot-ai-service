from pydantic import BaseModel, Field
from typing import List, Optional


class ProjectContext(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    fechaInicio: Optional[str] = None
    fechaFin: Optional[str] = None


class DocumentInput(BaseModel):
    type: str = Field(..., description="Document type, e.g. SRS or WBS")
    content: str = Field(..., description="Plain text content of the document")


class GenerateTasksRequest(BaseModel):
    projectId: str
    projectContext: ProjectContext
    documents: List[DocumentInput]
    maxHours: Optional[float] = None