import json

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Recommendation
from app.services.gemini_service import generate_recommendation


router = APIRouter(
    prefix="/planners",
    tags=["Planners"],
)


# -----------------------------
# Request Models
# -----------------------------

class HomeRequest(BaseModel):
    budget: float = Field(gt=0)
    room_type: str
    style: str = "Modern"
    requirements: str = ""


class PartyRequest(BaseModel):
    budget: float = Field(gt=0)
    event_type: str
    guests: int = Field(gt=0)
    venue: str = ""
    requirements: str = ""


class JewelryRequest(BaseModel):
    budget: float = Field(gt=0)
    occasion: str
    style: str = "Elegant"
    outfit_description: str = ""


# -----------------------------
# Save Recommendation
# -----------------------------

def save_recommendation(
    db: Session,
    category: str,
    budget: float,
    request_data: dict,
    result: str,
):
    recommendation = Recommendation(
        category=category,
        budget=budget,
        request_data=json.dumps(request_data),
        result=result,
    )

    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)

    return recommendation


# -----------------------------
# Status
# -----------------------------

@router.get("/status")
def planner_status():
    return {
        "status": "ok",
        "message": "Planner route is working",
    }


# -----------------------------
# Home Interior Planner
# -----------------------------

@router.post("/generate-home")
def generate_home(
    request: HomeRequest,
    db: Session = Depends(get_db),
):
    details = f"""
Room type: {request.room_type}
Style: {request.style}
Requirements: {request.requirements}
"""

    result = generate_recommendation(
        category="Home Interior",
        budget=request.budget,
        details=details,
    )

    saved = save_recommendation(
        db=db,
        category="home",
        budget=request.budget,
        request_data=request.model_dump(),
        result=result,
    )

    return {
        "success": True,
        "recommendation_id": saved.id,
        "category": "home",
        "budget": request.budget,
        "recommendation": result,
    }


# -----------------------------
# Party Planner
# -----------------------------

@router.post("/generate-party")
def generate_party(
    request: PartyRequest,
    db: Session = Depends(get_db),
):
    details = f"""
Event type: {request.event_type}
Number of guests: {request.guests}
Venue: {request.venue}
Requirements: {request.requirements}
"""

    result = generate_recommendation(
        category="Party Planning",
        budget=request.budget,
        details=details,
    )

    saved = save_recommendation(
        db=db,
        category="party",
        budget=request.budget,
        request_data=request.model_dump(),
        result=result,
    )

    return {
        "success": True,
        "recommendation_id": saved.id,
        "category": "party",
        "budget": request.budget,
        "recommendation": result,
    }


# -----------------------------
# Jewelry Planner
# -----------------------------

@router.post("/generate-jewelry")
def generate_jewelry(
    request: JewelryRequest,
    db: Session = Depends(get_db),
):
    details = f"""
Occasion: {request.occasion}
Style preference: {request.style}
Outfit description: {request.outfit_description}
"""

    result = generate_recommendation(
        category="Jewelry",
        budget=request.budget,
        details=details,
    )

    saved = save_recommendation(
        db=db,
        category="jewelry",
        budget=request.budget,
        request_data=request.model_dump(),
        result=result,
    )

    return {
        "success": True,
        "recommendation_id": saved.id,
        "category": "jewelry",
        "budget": request.budget,
        "recommendation": result,
    }


# -----------------------------
# Recommendation History
# -----------------------------

@router.get("/history")
def recommendation_history(
    db: Session = Depends(get_db),
):
    recommendations = (
        db.query(Recommendation)
        .order_by(
            Recommendation.created_at.desc()
        )
        .all()
    )

    return [
        {
            "id": item.id,
            "category": item.category,
            "budget": item.budget,
            "request_data": item.request_data,
            "result": item.result,
            "created_at": item.created_at,
        }
        for item in recommendations
    ]