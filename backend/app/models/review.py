from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewCreate(BaseModel):
    product_id: int
    user_id: Optional[str] = None
    user_name: str
    rating: int  # 1-5
    comment: str

class Review(BaseModel):
    id: int
    product_id: int
    user_id: Optional[str]
    user_name: str
    rating: int
    comment: str
    created_at: datetime
