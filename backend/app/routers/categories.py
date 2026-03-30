from fastapi import APIRouter

router = APIRouter(prefix="/categories", tags=["categories"])

CATEGORIES = [
    {"id": "ao", "name": "Áo"},
    {"id": "quan", "name": "Quần"},
    {"id": "vay", "name": "Váy & Đầm"},
]

@router.get("")
def get_categories():
    return CATEGORIES
