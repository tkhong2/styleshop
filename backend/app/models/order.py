from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderItem(BaseModel):
    product_id: int
    size: str
    color: str
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItem]
    total: int
    coupon: Optional[str] = None
    payment_method: Optional[str] = "cod"
    user_id: Optional[str] = None  # email của user

class Order(BaseModel):
    id: int
    items: List[OrderItem]
    total: int
    coupon: Optional[str]
    status: str
    payment_method: str
    payment_status: str
    transfer_note: Optional[str]
    user_id: Optional[str] = None
    created_at: datetime
