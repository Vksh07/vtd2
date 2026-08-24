from fastapi import APIRouter
from pydantic import BaseModel
import random

router = APIRouter()

class DrillRequest(BaseModel):
    topic: str
    count: int = 3
    weak_topics: list[str] = []
    strong_topics: list[str] = []

class DrillItem(BaseModel):
    id: int
    topic: str
    prompt: str
    options: list[str]
    answer: str
    explanation: str

BANK = [
    DrillItem(id=1, topic="Number System", prompt="If 3x + 5 = 20, what is x?", options=["4", "5", "6", "7"], answer="B", explanation="Subtract 5, then divide by 3: x = 5."),
    DrillItem(id=2, topic="Time Speed Distance", prompt="A train travels 60 km in 45 mins. Speed in km/h is?", options=["60", "75", "80", "90"], answer="C", explanation="Convert 45 mins to 0.75 hour; 60 / 0.75 = 80."),
    DrillItem(id=3, topic="Percentages", prompt="What is 15% of 240?", options=["30", "36", "40", "45"], answer="B", explanation="15% of 240 = 0.15 * 240 = 36."),
    DrillItem(id=4, topic="Ratio", prompt="The ratio of A:B is 3:2 and B:C is 4:3. Find A:C.", options=["2:1", "3:2", "4:3", "6:5"], answer="A", explanation="Scale to common B: 3:2 :: 6:4, so A:C = 6:4 = 3:2."),
    DrillItem(id=5, topic="Averages", prompt="Average of 4 numbers is 20. Sum is?", options=["60", "70", "80", "90"], answer="C", explanation="Sum = average * count = 20 * 4 = 80."),
    DrillItem(id=6, topic="Number System", prompt="What is the remainder when 123 is divided by 8?", options=["1", "2", "3", "4"], answer="C", explanation="8 * 15 = 120; 123 - 120 = 3."),
    DrillItem(id=7, topic="Time Speed Distance", prompt="If speed is doubled, time taken becomes?", options=["Half", "Double", "Same", "Triple"], answer="A", explanation="Time is inversely proportional to speed for fixed distance."),
    DrillItem(id=8, topic="Percentages", prompt="If 40% of a number is 80, the number is?", options=["180", "200", "220", "240"], answer="B", explanation="Number = 80 / 0.40 = 200."),
    DrillItem(id=9, topic="Ratio", prompt="Divide 100 in the ratio 2:3. Larger part is?", options=["40", "50", "60", "70"], answer="C", explanation="2+3=5 parts; larger part = 3/5 * 100 = 60."),
    DrillItem(id=10, topic="Averages", prompt="Average of 5 numbers is 30. Sum is?", options=["120", "150", "180", "200"], answer="B", explanation="Sum = 30 * 5 = 150."),
    DrillItem(id=11, topic="Number System", prompt="What is the LCM of 12 and 15?", options=["30", "45", "60", "90"], answer="C", explanation="LCM of 12 and 15 is 60."),
    DrillItem(id=12, topic="Time Speed Distance", prompt="A car covers 120 km in 2 hours. Speed is?", options=["50", "60", "70", "80"], answer="B", explanation="Speed = distance / time = 120 / 2 = 60."),
    DrillItem(id=13, topic="Percentages", prompt="A number increases by 20% and then decreases by 20%. Net change?", options=["0%", "-4%", "+4%", "-2%"], answer="B", explanation="Overall multiplier = 1.2 * 0.8 = 0.96, so -4%."),
    DrillItem(id=14, topic="Ratio", prompt="If A:B = 5:3 and B:C = 3:4, find A:C.", options=["5:4", "3:4", "5:3", "4:5"], answer="A", explanation="Common B=3 gives A:C = 5:4."),
    DrillItem(id=15, topic="Averages", prompt="Average of 3 numbers is 15. Sum is?", options=["30", "45", "60", "75"], answer="B", explanation="Sum = 15 * 3 = 45."),
    DrillItem(id=16, topic="Averages", prompt="The average of 5 consecutive even numbers is 30. Largest number is?", options=["32", "34", "36", "38"], answer="B", explanation="Sum = 30*5 = 150; numbers are 26,28,30,32,34; largest = 34."),
    DrillItem(id=17, topic="Time Speed Distance", prompt="Two trains 120 km apart move toward each other at 40 km/h and 60 km/h. Meeting time?", options=["1.2 h", "1.5 h", "2.0 h", "2.4 h"], answer="A", explanation="Relative speed = 100 km/h; time = 120/100 = 1.2 h."),
    DrillItem(id=18, topic="Percentages", prompt="If a value decreases by 10% twice, total decrease is?", options=["19%", "20%", "21%", "22%"], answer="A", explanation="Multiplier = 0.9*0.9 = 0.81, so decrease = 19%."),
    DrillItem(id=19, topic="Number System", prompt="Which number is divisible by both 3 and 4?", options=["22", "36", "45", "58"], answer="B", explanation="LCM of 3 and 4 is 12; 36 is divisible by 12."),
    DrillItem(id=20, topic="Ratio", prompt="In a 40L mixture of milk:water = 3:1, how much water to add for 1:1 ratio?", options=["10 L", "15 L", "20 L", "25 L"], answer="C", explanation="Milk = 30L, water = 10L; need 30L water, so add 20L."),
]

@router.post("/drill", response_model=list[DrillItem])
def generate_drill(req: DrillRequest):
    topic = (req.topic or "").strip().lower()
    weak = [t.strip().lower() for t in req.weak_topics if t and t.strip()]
    strong = [t.strip().lower() for t in req.strong_topics if t and t.strip()]

    if topic:
        filtered = [q for q in BANK if q.topic.lower() == topic]
        if not filtered:
            filtered = list(BANK)
        count = max(1, min(req.count, len(filtered)))
        return random.sample(filtered, count)

    weak_items = [q for q in BANK if q.topic.lower() in weak]
    strong_items = [q for q in BANK if q.topic.lower() in strong and q.topic.lower() not in weak]
    general_items = [q for q in BANK if q.topic.lower() not in weak and q.topic.lower() not in strong]

    if weak_items:
        weak_count = max(1, int(round(req.count * 0.65)))
        strong_count = max(0, int(round(req.count * 0.2)))
        general_count = max(0, req.count - weak_count - strong_count)

        selected = []
        selected.extend(random.sample(weak_items, min(weak_count, len(weak_items))))
        if strong_items:
            selected.extend(random.sample(strong_items, min(strong_count, len(strong_items))))
        if general_items:
            selected.extend(random.sample(general_items, min(general_count, len(general_items))))

        remaining = req.count - len(selected)
        if remaining > 0:
            pool = [q for q in BANK if q not in selected]
            if pool:
                selected.extend(random.sample(pool, min(remaining, len(pool))))

        return selected[: req.count]

    filtered = list(BANK)
    count = max(1, min(req.count, len(filtered)))
    return random.sample(filtered, count)
