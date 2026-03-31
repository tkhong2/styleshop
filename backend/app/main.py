from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.routers import products, orders, categories, reviews

load_dotenv()

app = FastAPI(title=os.getenv("APP_NAME", "StyleShop API"), version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
app.include_router(categories.router, prefix="/api")
app.include_router(reviews.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "StyleShop API is running", "docs": "/docs"}

@app.get("/health")
def health():
    """Kiểm tra kết nối DB"""
    import os
    db_url = os.environ.get("DATABASE_URL", "NOT SET")
    db_type = "postgresql" if db_url.startswith("postgres") else "sqlite"
    try:
        from app.database import load_orders
        orders = load_orders()
        return {"status": "ok", "db_type": db_type, "orders_count": len(orders), "db_url_prefix": db_url[:30] + "..."}
    except Exception as e:
        return {"status": "error", "db_type": db_type, "error": str(e)}
