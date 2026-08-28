from fastapi import FastAPI

app=FastAPI(
    title="E-Commerce API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message":"Ecommerce api is running ."
    }
