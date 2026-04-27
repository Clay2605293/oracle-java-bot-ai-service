import json
from pathlib import Path
from typing import Optional

from openai import OpenAI
from app.core.config import settings
from app.models.response_models import GeneratedTask

client = OpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "task_generation_system_prompt.md"
SYSTEM_PROMPT = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").strip()

# Fix 1: truncar a 6000 chars para no saturar el contexto
MAX_CONTENT_CHARS = 6000


def generate_tasks_with_openai(
    content: str,
    max_hours: Optional[float] = None
) -> list[GeneratedTask]:
    truncated = content[:MAX_CONTENT_CHARS]
    normalized_max_hours = normalize_max_hours(max_hours)

    user_prompt = build_user_prompt(truncated, normalized_max_hours)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_completion_tokens=2000
    )

    raw = response.choices[0].message.content.strip()

    # Fix 2: limpiar markdown fences si OpenAI los incluye
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    print(f"🔍 OpenAI raw response (first 200 chars): {raw[:200]}", flush=True)

    if not raw:
        print("❌ OpenAI returned empty response", flush=True)
        return []

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}", flush=True)
        print(f"❌ Full raw response: {raw}", flush=True)
        return []

    tasks = []
    for t in data:
        if not isinstance(t, dict):
            continue

        tasks.append(GeneratedTask(
            titulo=str(t.get("titulo", "Sin título"))[:120],
            descripcion=str(t.get("descripcion", ""))[:500],
            tiempoEstimado=parse_tiempo_estimado(t.get("tiempoEstimado"))
        ))

    tasks = enforce_total_hours_limit(tasks, normalized_max_hours)

    total_hours = sum(
        task.tiempoEstimado or 0
        for task in tasks
    )

    print(
        f"⏱️ Generated {len(tasks)} tasks with total estimated hours: {total_hours}"
        + (f" / maxHours: {normalized_max_hours}" if normalized_max_hours else ""),
        flush=True
    )

    return tasks


def build_user_prompt(content: str, max_hours: Optional[float]) -> str:
    if max_hours is None:
        return f"Genera tareas de backlog para este proyecto:\n\n{content}"

    return (
        f"Genera tareas de backlog para este proyecto.\n\n"
        f"Restricción obligatoria:\n"
        f"- La suma total de tiempoEstimado de todas las tareas generadas no debe exceder {max_hours} horas.\n"
        f"- Si no puedes cubrir todo el documento dentro de ese límite, prioriza las tareas más importantes.\n"
        f"- No generes tareas adicionales si hacerlo supera el límite total de horas.\n\n"
        f"Documento del proyecto:\n\n{content}"
    )


def normalize_max_hours(max_hours: Optional[float]) -> Optional[float]:
    if max_hours is None:
        return None

    try:
        value = float(max_hours)
    except (TypeError, ValueError):
        return None

    if value <= 0:
        return None

    return value


def parse_tiempo_estimado(value) -> Optional[float]:
    if value is None:
        return None

    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None

    if parsed <= 0:
        return None

    return parsed


def enforce_total_hours_limit(
    tasks: list[GeneratedTask],
    max_hours: Optional[float]
) -> list[GeneratedTask]:
    if max_hours is None:
        return tasks

    accepted_tasks = []
    accumulated_hours = 0.0

    for task in tasks:
        estimated = task.tiempoEstimado

        if estimated is None:
            # Para que el límite sea auditable, no aceptamos tareas sin estimación
            # cuando maxHours viene definido.
            continue

        if accumulated_hours + estimated <= max_hours:
            accepted_tasks.append(task)
            accumulated_hours += estimated
        else:
            print(
                f"⚠️ Skipping task because it exceeds maxHours: {task.titulo} ({estimated}h)",
                flush=True
            )

    return accepted_tasks