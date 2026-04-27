import json

from openai import OpenAI

from app.core.config import settings
from app.models.response_models import GeneratedTask

client = OpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT = """
Eres un experto en gestion de proyectos de software.
Tu tarea es generar tareas de backlog a partir de documentos de requerimientos.
Responde UNICAMENTE con un JSON array. Sin texto adicional, sin markdown, sin bloques de codigo.
Schema de cada tarea:
{
  "titulo": "string (maximo 120 caracteres)",
  "descripcion": "string (maximo 500 caracteres)",
  "tiempoEstimado": float o null (horas de trabajo estimadas)
}
"""


def generate_tasks_with_openai(content: str) -> list[GeneratedTask]:
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Genera tareas de backlog para este proyecto:\n\n{content}"},
        ],
        max_completion_tokens=2000,
    )

    raw = (response.choices[0].message.content or "").strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print(f"OpenAI returned invalid JSON: {raw}", flush=True)
        return []

    tasks = []
    for t in data:
        if not isinstance(t, dict):
            continue

        tasks.append(
            GeneratedTask(
                titulo=str(t.get("titulo", "Sin titulo"))[:120],
                descripcion=str(t.get("descripcion", ""))[:500],
                tiempoEstimado=t.get("tiempoEstimado"),
            )
        )

    return tasks
