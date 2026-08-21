from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class EthicsRequest(BaseModel):
    question: str

class EthicsTemplate(BaseModel):
    intro: str
    body_points: list[str]
    conclusion: str

def pick_template(question: str) -> EthicsTemplate:
    q = question.lower()
    if "public servant" in q or "civil servant" in q or "upsc" in q or "service" in q:
        return EthicsTemplate(
            intro="Public service ethics revolve around accountability, neutrality, and public trust.",
            body_points=[
                "Discuss constitutional values and rule of law.",
                "Explain conflict of interest and impartiality.",
                "Use case examples from governance or administration.",
            ],
            conclusion="A balanced ethical conclusion should prioritize public interest while respecting procedural fairness.",
        )
    if "environment" in q or "climate" in q or "sustainability" in q:
        return EthicsTemplate(
            intro="Environmental ethics require balancing development with intergenerational justice.",
            body_points=[
                "State the ethical dilemma between growth and sustainability.",
                "Apply principles of stewardship and equity.",
                "Refer to policies, court judgments, or international commitments.",
            ],
            conclusion="Ethical environmental action combines regulation, innovation, and citizen responsibility.",
        )
    if "technology" in q or "ai" in q or "data" in q or "digital" in q:
        return EthicsTemplate(
            intro="Technology ethics must address privacy, bias, accountability, and consent.",
            body_points=[
                "Identify the stakeholder risks in the technology.",
                "Evaluate fairness, transparency, and autonomy.",
                "Suggest governance and regulatory safeguards.",
            ],
            conclusion="Technology should advance human dignity, not erode it.",
        )
    if "family" in q or "caste" in q or "gender" in q or "minority" in q:
        return EthicsTemplate(
            intro="Social ethics demand equality, dignity, and protection from structural harm.",
            body_points=[
                "Describe the social inequity or discrimination involved.",
                "Use constitutional morality and human rights framing.",
                "Link to policy, reform, or restorative justice.",
            ],
            conclusion="Ethical progress requires both legal safeguards and social transformation.",
        )
    return EthicsTemplate(
        intro="Ethical analysis begins with clarifying values, facts, and competing duties.",
        body_points=[
            "Identify the core ethical conflict.",
            "Apply relevant ethical frameworks or constitutional values.",
            "Weigh stakeholder interests and likely consequences.",
        ],
        conclusion="A good ethical answer ends with a clear, principled, and practical recommendation.",
    )

@router.post("/template", response_model=EthicsTemplate)
def generate_template(req: EthicsRequest):
    return pick_template(req.question or "General ethics")
