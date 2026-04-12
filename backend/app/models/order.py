from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class OrderItem(BaseModel):
    product_id: int
    name: Optional[str] = None
    price: Optional[int] = None
    size: str
    color: str
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItem]
    total: int
    coupon: Optional[str] = None
    payment_method: Optional[str] = "cod"
    user_id: Optional[str] = None  # email của user
    shipping: Optional[Dict[str, Any]] = None  # thông tin giao hàng

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
    shipping: Optional[Dict[str, Any]] = None
    created_at: datetime
