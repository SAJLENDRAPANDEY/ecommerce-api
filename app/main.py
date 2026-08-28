from fastapi import FastAPI
from app.routers import products




app=FastAPI(
    title="E-Commerce API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message":"Ecommerce api is running ."
    }

@app.get("/health")
def health_check():
    return {
        "status":"Healthy"
    }


app.include_router(products.router)