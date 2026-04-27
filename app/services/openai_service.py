import json
from pathlib import Path

from openai import OpenAI
from app.core.config import settings
from app.models.response_models import GeneratedTask

client = OpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "task_generation_system_prompt.md"
SYSTEM_PROMPT = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").strip()

# Fix 1: truncar a 6000 chars para no saturar el contexto
MAX_CONTENT_CHARS = 6000


def generate_tasks_with_openai(content: str) -> list[GeneratedTask]:
    truncated = content[:MAX_CONTENT_CHARS]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Genera tareas de backlog para este proyecto:\n\n{truncated}"}
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
            tiempoEstimado=t.get("tiempoEstimado")
        ))

    return tasks