from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Plan(BaseModel):
    name: str
    price_inr: int
    currency: str = "INR"
    includes_report: bool = True
    includes_tutor: bool = False
    support: str


class PlanResponse(BaseModel):
    plans: list[Plan]


@router.get("/", response_model=PlanResponse)
def get_pricing():
    return PlanResponse(
        plans=[
            Plan(
                name="Starter",
                price_inr=199,
                includes_report=True,
                includes_tutor=False,
                support="email support",
            ),
            Plan(
                name="Aspirant",
                price_inr=499,
                includes_report=True,
                includes_tutor=True,
                support="priority chat support",
            ),
            Plan(
                name="Mentor",
                price_inr=999,
                includes_report=True,
                includes_tutor=True,
                support="dedicated mentor session",
            ),
        ]
    )


@router.get("", response_model=PlanResponse, include_in_schema=False)
def pricing_redirect():
    return get_pricing()
