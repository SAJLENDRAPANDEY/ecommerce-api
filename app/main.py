from fastapi import FastAPI

from app.routers import products
from app.routers.auth import router as auth_router
from app.routers.cart import router as cart_router
from app.routers.orders import router as orders_router

from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order, OrderItem


app = FastAPI(
    title="E-Commerce API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Ecommerce api is running."
    }


@app.get("/health")
def health_check():
    return {
        "status": "Healthy"
    }


app.include_router(products.router)
app.include_router(auth_router)
app.include_router(cart_router)
app.include_router(orders_router)