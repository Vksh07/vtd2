from fastapi import APIRouter
from pydantic import BaseModel
from collections import defaultdict

router = APIRouter()

class Attempt(BaseModel):
    topic: str
    correct: bool

class WeakAreasRequest(BaseModel):
    attempts: list[Attempt]

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
        topic = (a.topic or "").strip()
        if not topic:
            continue
        stats[topic]["total"] += 1
        if a.correct:
            stats[topic]["correct"] += 1

    items = []
    for topic, s in stats.items():
        accuracy = s["correct"] / s["total"] if s["total"] else 0.0
        items.append(TopicStat(topic=topic, total=s["total"], correct=s["correct"], accuracy=accuracy))

    weak = sorted([i for i in items if i.accuracy < 0.7], key=lambda i: (i.accuracy, i.total), reverse=False)
    strong = sorted([i for i in items if i.accuracy >= 0.7], key=lambda i: (i.accuracy, i.total), reverse=True)
    return WeakAreasResponse(weak=weak, strong=strong)
