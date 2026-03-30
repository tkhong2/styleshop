from pydantic import BaseModel
from typing import List, Optional

class Product(BaseModel):
    id: int
    name: str
    price: int
    original_price: int
    category: str          # ao | quan | vay
    gender: str            # nam | nu | unisex
    image: str
    images: List[str]
    sizes: List[str]
    colors: List[str]
    description: str
    rating: float
    reviews: int
    is_new: bool
    is_sale: bool
