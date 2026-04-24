from app.models.request_models import GenerateTasksRequest
from app.models.response_models import GenerateTasksResponse, GeneratedTask


class TaskGenerationService:

    # 🔵 REST (ya lo tienes)
    def generate_tasks(self, request: GenerateTasksRequest) -> GenerateTasksResponse:
        return self._generate_sample_tasks(
            source=request.documents[0].type if request.documents else "UNKNOWN"
        )

    # 🟡 Kafka (nuevo)
    def generate_tasks_from_kafka(self, request_dict: dict) -> dict:

        documents = request_dict.get("documents", [])

        source = documents[0].get("type") if documents else "UNKNOWN"

        response = self._generate_sample_tasks(source)

        # 🔥 OJO: Kafka trabaja mejor con dict, no con Pydantic
        return {
            "projectId": request_dict.get("projectId"),
            "tasks": [task.dict() for task in response.tasks]
        }

    # 🧠 lógica compartida
    def _generate_sample_tasks(self, source: str) -> GenerateTasksResponse:

        sample_tasks = [
            GeneratedTask(
                titulo="Definir modelo inicial de backlog IA",
                descripcion="Diseñar la estructura de datos para tareas generadas automáticamente.",
                priority="HIGH",
                estimatedHours=6.0,
                suggestedDeadlineOffsetDays=3,
                source=source
            ),
            GeneratedTask(
                titulo="Implementar endpoint de generación de tareas",
                descripcion="Crear el endpoint principal para procesar documentos y devolver tareas sugeridas.",
                priority="HIGH",
                estimatedHours=8.0,
                suggestedDeadlineOffsetDays=5,
                source=source
            )
        ]

        return GenerateTasksResponse(tasks=sample_tasks)