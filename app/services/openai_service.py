import json
from pathlib import Path
from typing import Optional

from openai import OpenAI
from app.core.config import settings
from app.models.response_models import GeneratedTask, DuplicateCandidate

client = OpenAI(api_key=settings.OPENAI_API_KEY)

TASK_GENERATION_SYSTEM_PROMPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "prompts"
    / "task_generation_system_prompt.md"
)

DUPLICATE_DETECTION_SYSTEM_PROMPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "prompts"
    / "duplicate_detection_system_prompt.md"
)

SYSTEM_PROMPT = TASK_GENERATION_SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").strip()
DUPLICATE_DETECTION_SYSTEM_PROMPT = DUPLICATE_DETECTION_SYSTEM_PROMPT_PATH.read_text(
    encoding="utf-8"
).strip()

MAX_CONTENT_CHARS = 6000
MAX_TASK_DESCRIPTION_CHARS = 350


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
    raw = clean_json_response(raw)

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


def detect_duplicate_tasks_with_openai(
    tasks: list[dict],
    threshold: Optional[float] = 0.80
) -> list[DuplicateCandidate]:
    normalized_threshold = normalize_threshold(threshold)
    compact_tasks = compact_duplicate_detection_tasks(tasks)

    user_prompt = build_duplicate_detection_prompt(
        compact_tasks,
        normalized_threshold
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": DUPLICATE_DETECTION_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1,
        max_completion_tokens=2500
    )

    raw = response.choices[0].message.content.strip()
    raw = clean_json_response(raw)

    print(f"🔍 Duplicate detection raw response (first 300 chars): {raw[:300]}", flush=True)

    if not raw:
        print("⚠️ OpenAI returned empty duplicate detection response", flush=True)
        return []

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"❌ Duplicate detection JSON parse error: {e}", flush=True)
        print(f"❌ Full raw response: {raw}", flush=True)
        return []

    if not isinstance(data, list):
        print("⚠️ Duplicate detection response was not a JSON array", flush=True)
        return []

    duplicates = []

    for item in data:
        if not isinstance(item, dict):
            continue

        score = parse_similarity_score(item.get("similarityScore"))

        if score < normalized_threshold:
            continue

        task_a_id = str(item.get("taskAId", "")).strip()
        task_b_id = str(item.get("taskBId", "")).strip()

        if not task_a_id or not task_b_id:
            continue

        if task_a_id == task_b_id:
            continue

        duplicates.append(DuplicateCandidate(
            taskAId=task_a_id,
            taskBId=task_b_id,
            taskATitle=str(item.get("taskATitle", ""))[:120],
            taskBTitle=str(item.get("taskBTitle", ""))[:120],
            similarityScore=score,
            reason=str(item.get("reason", ""))[:1000]
        ))

    print(
        f"🔁 Duplicate candidates detected: {len(duplicates)} "
        f"with threshold {normalized_threshold}",
        flush=True
    )

    return duplicates


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


def build_duplicate_detection_prompt(
    tasks: list[dict],
    threshold: float
) -> str:
    return (
        "Analiza las siguientes tareas de un proyecto y detecta pares posiblemente duplicados.\n\n"
        f"Threshold mínimo requerido: {threshold}\n\n"
        "Tareas:\n"
        f"{json.dumps(tasks, ensure_ascii=False, indent=2)}\n\n"
        "Devuelve únicamente un arreglo JSON válido con los pares duplicados."
    )


def compact_duplicate_detection_tasks(tasks: list[dict]) -> list[dict]:
    compact = []

    for task in tasks:
        if not isinstance(task, dict):
            continue

        task_id = str(task.get("taskId", "")).strip()
        title = str(task.get("titulo", "")).strip()
        description = str(task.get("descripcion", "") or "").strip()

        if not task_id or not title:
            continue

        compact.append({
            "taskId": task_id,
            "titulo": title[:120],
            "descripcion": description[:MAX_TASK_DESCRIPTION_CHARS]
        })

    return compact


def clean_json_response(raw: str) -> str:
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    return raw


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


def normalize_threshold(threshold: Optional[float]) -> float:
    if threshold is None:
        return 0.80

    try:
        value = float(threshold)
    except (TypeError, ValueError):
        return 0.80

    if value < 0:
        return 0.0

    if value > 1:
        return 1.0

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


def parse_similarity_score(value) -> float:
    if value is None:
        return 0.0

    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return 0.0

    if parsed < 0:
        return 0.0

    if parsed > 1:
        return 1.0

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