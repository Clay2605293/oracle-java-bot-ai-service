from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.ai import router as ai_router

app = FastAPI(
    title="Oracle Java Bot AI Service",
    version="0.1.0",
    description="AI pipeline service for backlog generation and optimization."
)

app.include_router(health_router)
app.include_router(ai_router)