from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from pathlib import Path

app = FastAPI()

# Загрузка датасета один раз при старте
DATASET_PATH = Path(__file__).parent.parent.parent / "data" / "processed" / "skills_dataset.json"

try:
    with DATASET_PATH.open("r", encoding="utf-8") as f:
        ROLES = json.load(f)
except FileNotFoundError:
    ROLES = []

class StudentProfile(BaseModel):
    skills: list[str]
    interests: list[str] | None = None

@app.post("/recommendations")
def get_recommendations(profile: StudentProfile):
    if not ROLES:
        raise HTTPException(status_code=500, detail="Dataset not found")

    student_skills = set(s.lower() for s in profile.skills)
    
    # Простая логика: считаем пересечение навыков с каждой ролью
    scored_roles = []
    for role in ROLES:
        role_skills = set(s.lower() for s in role["required_skills"])
        intersection = student_skills & role_skills
        score = len(intersection)
        if score > 0:
            scored_roles.append({
                "role": role["role"],
                "score": score,
                "recommended_courses": role["recommended_courses"],
                "extra_skills": role["extra_skills"]
            })

    # Сортируем по количеству совпадений
    scored_roles.sort(key=lambda x: x["score"], reverse=True)

    # Возвращаем топ-3 роли и собираем рекомендации
    top_roles = scored_roles[:3]
    all_courses = []
    all_extra = []
    seen_courses = set()
    seen_extra = set()

    for r in top_roles:
        for c in r["recommended_courses"]:
            if c not in seen_courses:
                seen_courses.add(c)
                all_courses.append(c)
        for s in r["extra_skills"]:
            if s not in seen_extra:
                seen_extra.add(s)
                all_extra.append(s)

    return {
        "top_roles": [r["role"] for r in top_roles],
        "recommended_courses": all_courses[:5],
        "additional_skills": all_extra[:5],
        "match_details": top_roles
    }

@app.get("/health")
def health():
    return {"status": "ok", "roles_count": len(ROLES)}
