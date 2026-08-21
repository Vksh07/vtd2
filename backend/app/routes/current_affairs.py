from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class CurrentAffairsRequest(BaseModel):
    headline: str

class CurrentAffairsResponse(BaseModel):
    gs_mapping: str
    answer_outline: list[str]
    keywords: list[str]

@router.post("/map", response_model=CurrentAffairsResponse)
def map_headline(req: CurrentAffairsRequest):
    headline = req.headline.strip()
    gs_mapping = "Likely GS-II/III: Polity/Governance/IR depending on context."
    answer_outline = [
        "Context: What the headline means.",
        "Stakeholders: Who is affected.",
        "Implications: Short-term and long-term.",
        "Conclusion: Balanced view with examples.",
    ]
    keywords = [word.lower() for word in headline.split() if len(word) > 4][:5]
    return CurrentAffairsResponse(
        gs_mapping=gs_mapping,
        answer_outline=answer_outline,
        keywords=keywords,
    )
