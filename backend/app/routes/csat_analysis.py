from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from collections import defaultdict

router = APIRouter()

class Attempt(BaseModel):
    topic: str
    correct: bool

    @validator("topic")
    def topic_not_empty(cls, value: str):
        if not value or not value.strip():
            raise ValueError("topic must not be empty")
        return value.strip()

    @validator("correct")
    def correct_must_be_bool(cls, value):
        if not isinstance(value, bool):
            raise ValueError("correct must be a boolean")
        return value

class WeakAreasRequest(BaseModel):
    attempts: list[Attempt]

    @validator("attempts")
    def attempts_not_empty(cls, value):
        if not value:
            raise ValueError("attempts must not be empty")
        if len(value) > 500:
            raise ValueError("attempts must not exceed 500")
        return value

class TopicStat(BaseModel):
    topic: str
    total: int
    correct: int
    accuracy: float

class WeakAreasResponse(BaseModel):
    weak: list[TopicStat]
    strong: list[TopicStat]

@router.post("/weak-areas", response_model=WeakAreasResponse)
def weak_areas(req: WeakAreasRequest):
    stats: dict[str, dict[str, int]] = defaultdict(lambda: {"total": 0, "correct": 0})
    for a in req.attempts:
        stats[a.topic]["total"] += 1
        if a.correct:
            stats[a.topic]["correct"] += 1

    items = []
    for topic, s in stats.items():
        accuracy = s["correct"] / s["total"] if s["total"] else 0.0
        items.append(TopicStat(topic=topic, total=s["total"], correct=s["correct"], accuracy=accuracy))

    weak = sorted([i for i in items if i.accuracy < 0.7], key=lambda i: (i.accuracy, i.total), reverse=False)
    strong = sorted([i for i in items if i.accuracy >= 0.7], key=lambda i: (i.accuracy, i.total), reverse=True)
    return WeakAreasResponse(weak=weak, strong=strong)
