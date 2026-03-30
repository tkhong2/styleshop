from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.routers import products, orders, categories

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

@app.get("/")
def root():
    return {"message": "StyleShop API is running", "docs": "/docs"}
