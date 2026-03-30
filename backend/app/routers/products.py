from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.data import PRODUCTS
from app.models.product import Product

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=List[Product])
def get_products(
    category: Optional[str] = Query(None),
    gender: Optional[str] = Query(None),
    is_sale: Optional[bool] = Query(None),
    is_new: Optional[bool] = Query(None),
    q: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
):
    result = PRODUCTS

    if q:
        lower = q.lower()
        result = [p for p in result if lower in p.name.lower() or lower in p.description.lower() or lower in p.category.lower()]
    if category:
        result = [p for p in result if p.category == category]
    if gender:
        result = [p for p in result if p.gender == gender or p.gender == "unisex"]
    if is_sale is not None:
        result = [p for p in result if p.is_sale == is_sale]
    if is_new is not None:
        result = [p for p in result if p.is_new == is_new]

    return result[skip : skip + limit]

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = next((p for p in PRODUCTS if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
    return product
