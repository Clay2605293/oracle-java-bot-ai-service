import json
import math
from typing import Optional

from openai import OpenAI

from app.core.config import settings


EMBEDDING_MODEL = "text-embedding-3-small"


class SemanticDuplicateDetectionService:

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def detect_semantic_duplicates_from_kafka(self, request_dict: dict) -> dict:
        try:
            run_id = request_dict.get("runId")
            project_id = request_dict.get("projectId")
            threshold = self._normalize_threshold(request_dict.get("threshold"))
            requested_model = request_dict.get("embeddingModel") or EMBEDDING_MODEL
            tasks = request_dict.get("tasks", [])

            print(
                f"🧠 Starting semantic duplicate detection for project {project_id} "
                f"with {len(tasks)} tasks. Threshold: {threshold}",
                flush=True
            )

            compact_tasks = self._compact_tasks(tasks)

            if len(compact_tasks) < 2:
                return {
                    "runId": run_id,
                    "projectId": project_id,
                    "status": "COMPLETED",
                    "errorMessage": None,
                    "embeddingModel": requested_model,
                    "embeddings": [],
                    "duplicates": []
                }

            embeddings = self._generate_embeddings(compact_tasks, requested_model)
            duplicates = self._find_duplicate_candidates(compact_tasks, embeddings, threshold)

            print(
                f"🧠 Semantic duplicate candidates detected: {len(duplicates)}",
                flush=True
            )

            return {
                "runId": run_id,
                "projectId": project_id,
                "status": "COMPLETED",
                "errorMessage": None,
                "embeddingModel": requested_model,
                "embeddings": [],
                "duplicates": duplicates
            }

        except Exception as e:
            print(f"❌ Semantic duplicate detection failed: {e}", flush=True)

            return {
                "runId": request_dict.get("runId"),
                "projectId": request_dict.get("projectId"),
                "status": "FAILED",
                "errorMessage": str(e),
                "embeddingModel": request_dict.get("embeddingModel") or EMBEDDING_MODEL,
                "embeddings": [],
                "duplicates": []
            }

    def _compact_tasks(self, tasks: list[dict]) -> list[dict]:
        compact = []

        for task in tasks:
            if not isinstance(task, dict):
                continue

            task_id = str(task.get("taskId", "")).strip()
            title = str(task.get("titulo", "")).strip()
            description = str(task.get("descripcion", "") or "").strip()

            if not task_id or not title:
                continue

            embedding_text = self._build_embedding_text(title, description)

            compact.append({
                "taskId": task_id,
                "titulo": title[:120],
                "descripcion": description[:500],
                "embeddingText": embedding_text[:1000]
            })

        return compact

    def _build_embedding_text(self, title: str, description: str) -> str:
        if description:
            return f"Título: {title}\nDescripción: {description}"

        return f"Título: {title}"

    def _generate_embeddings(
        self,
        tasks: list[dict],
        model: str
    ) -> list[dict]:
        input_texts = [task["embeddingText"] for task in tasks]

        response = self.client.embeddings.create(
            model=model,
            input=input_texts
        )

        embeddings_by_index = response.data

        result = []

        for index, task in enumerate(tasks):
            result.append({
                "taskId": task["taskId"],
                "titulo": task["titulo"],
                "descripcion": task["descripcion"],
                "embeddingText": task["embeddingText"],
                "embedding": embeddings_by_index[index].embedding
            })

        return result

    def _find_duplicate_candidates(
        self,
        tasks: list[dict],
        embeddings: list[dict],
        threshold: float
    ) -> list[dict]:
        duplicates = []

        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                task_a = embeddings[i]
                task_b = embeddings[j]

                score = self._cosine_similarity(
                    task_a["embedding"],
                    task_b["embedding"]
                )

                if score >= threshold:
                    duplicates.append({
                        "taskAId": task_a["taskId"],
                        "taskBId": task_b["taskId"],
                        "taskATitle": task_a["titulo"][:120],
                        "taskBTitle": task_b["titulo"][:120],
                        "similarityScore": round(score, 4),
                        "reason": self._build_reason(task_a, task_b, score)
                    })

        duplicates.sort(key=lambda item: item["similarityScore"], reverse=True)

        return duplicates

    def _cosine_similarity(
        self,
        vector_a: list[float],
        vector_b: list[float]
    ) -> float:
        dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
        norm_a = math.sqrt(sum(a * a for a in vector_a))
        norm_b = math.sqrt(sum(b * b for b in vector_b))

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot_product / (norm_a * norm_b)

    def _build_reason(
        self,
        task_a: dict,
        task_b: dict,
        score: float
    ) -> str:
        return (
            f"Las tareas presentan alta similitud semántica "
            f"entre título y descripción. Score calculado por embeddings: {round(score, 4)}."
        )[:1000]

    def _normalize_threshold(self, threshold: Optional[float]) -> float:
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
