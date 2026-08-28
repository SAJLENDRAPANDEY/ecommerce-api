from fastapi import APIRouter
from app.schemas.product import ProductResponse

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

products = [
    {
        "id": 1,
        "name": "iPhone 15",
        "description": "Apple smartphone",
        "price": 69999,
        "stock": 10
    },
    {
        "id": 2,
        "name": "Samsung Galaxy S24",
        "description": "Samsung smartphone",
        "price": 64999,
        "stock": 15
    }
]


@router.get("/", response_model=list[ProductResponse])
def get_products():
    return products


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            return product