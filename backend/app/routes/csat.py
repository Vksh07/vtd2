from fastapi import APIRouter
from pydantic import BaseModel
import random

router = APIRouter()

class DrillRequest(BaseModel):
    topic: str
    count: int = 3

class DrillItem(BaseModel):
    id: int
    topic: str
    prompt: str
    options: list[str]
    answer: str

BANK = [
    DrillItem(id=1, topic="Number System", prompt="If 3x + 5 = 20, what is x?", options=["4", "5", "6", "7"], answer="B"),
    DrillItem(id=2, topic="Time Speed Distance", prompt="A train travels 60 km in 45 mins. Speed in km/h is?", options=["60", "75", "80", "90"], answer="C"),
    DrillItem(id=3, topic="Percentages", prompt="What is 15% of 240?", options=["30", "36", "40", "45"], answer="B"),
    DrillItem(id=4, topic="Ratio", prompt="The ratio of A:B is 3:2 and B:C is 4:3. Find A:C.", options=["2:1", "3:2", "4:3", "6:5"], answer="A"),
    DrillItem(id=5, topic="Averages", prompt="Average of 4 numbers is 20. Sum is?", options=["60", "70", "80", "90"], answer="C"),
    DrillItem(id=6, topic="Number System", prompt="What is the remainder when 245 is divided by 7?", options=["1", "2", "3", "4"], answer="A"),
    DrillItem(id=7, topic="Time Speed Distance", prompt="If speed is doubled, time taken becomes?", options=["Half", "Double", "Same", "Triple"], answer="A"),
    DrillItem(id=8, topic="Percentages", prompt="If 40% of a number is 80, the number is?", options=["180", "200", "220", "240"], answer="B"),
    DrillItem(id=9, topic="Ratio", prompt="Divide 100 in the ratio 2:3. Larger part is?", options=["40", "50", "60", "70"], answer="C"),
    DrillItem(id=10, topic="Averages", prompt="Average of 5 numbers is 30. Sum is?", options=["120", "150", "180", "200"], answer="B"),
    DrillItem(id=11, topic="Number System", prompt="What is the LCM of 12 and 15?", options=["30", "45", "60", "90"], answer="C"),
    DrillItem(id=12, topic="Time Speed Distance", prompt="A car covers 120 km in 2 hours. Speed is?", options=["50", "60", "70", "80"], answer="B"),
    DrillItem(id=13, topic="Percentages", prompt="A number increases by 20% and then decreases by 20%. Net change?", options=["0%", "-4%", "+4%", "-2%"], answer="B"),
    DrillItem(id=14, topic="Ratio", prompt="If A:B = 5:3 and B:C = 3:4, find A:C.", options=["5:4", "3:4", "5:3", "4:5"], answer="A"),
    DrillItem(id=15, topic="Averages", prompt="Average of 3 numbers is 15. Sum is?", options=["30", "45", "60", "75"], answer="B"),
]

@router.post("/drill", response_model=list[DrillItem])
def generate_drill(req: DrillRequest):
    topic = (req.topic or "").strip().lower()
    if topic:
        filtered = [q for q in BANK if q.topic.lower() == topic]
    else:
        filtered = list(BANK)
    if not filtered:
        filtered = list(BANK)
    count = max(1, min(req.count, len(filtered)))
    selected = random.sample(filtered, count)
    return selected
