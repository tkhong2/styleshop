from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List
from app.models.review import ReviewCreate, Review
from app.database import load_reviews, save_review

router = APIRouter(prefix="/reviews", tags=["reviews"])

_counter = 0

@router.get("/{product_id}", response_model=List[Review])
def get_reviews(product_id: int):
    return [Review(**r) for r in load_reviews(product_id)]

@router.post("", response_model=Review, status_code=201)
def create_review(payload: ReviewCreate):
    global _counter
    _counter += 1
    review_dict = {
        "id": _counter,
        "product_id": payload.product_id,
        "user_id": payload.user_id,
        "user_name": payload.user_name,
        "rating": max(1, min(5, payload.rating)),
        "comment": payload.comment,
        "created_at": datetime.utcnow().isoformat(),
    }
    save_review(review_dict)
    return Review(**review_dict)
