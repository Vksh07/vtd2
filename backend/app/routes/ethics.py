from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class EthicsRequest(BaseModel):
    question: str

class EthicsTemplate(BaseModel):
    intro: str
    body_points: list[str]
    conclusion: str

@router.post("/template", response_model=EthicsTemplate)
def generate_template(req: EthicsRequest):
    return EthicsTemplate(
        intro="Ethical analysis requires balancing facts, values, and stakeholders.",
        body_points=[
            "Define the ethical issue clearly.",
            "Apply relevant ethical frameworks.",
            "Consider short-term and long-term consequences.",
        ],
        conclusion="Conclusion should synthesize analysis and suggest a principled course of action.",
    )
