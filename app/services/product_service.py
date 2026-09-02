from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product





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


def get_all_products():
    return products


def get_product_by_id(product_id: int):

    for product in products:
        if product["id"] == product_id:
            return product

    return None


def create_product(product):

    new_id = max([p["id"] for p in products], default=0) + 1

    new_product = {
        "id": new_id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock
    }

    products.append(new_product)

    return new_product


def update_product(product_id: int, product):

    for item in products:

        if item["id"] == product_id:

            if product.name is not None:
                item["name"] = product.name

            if product.description is not None:
                item["description"] = product.description

            if product.price is not None:
                item["price"] = product.price

            if product.stock is not None:
                item["stock"] = product.stock

            return item

    return None


def delete_product(product_id: int):

    for index, product in enumerate(products):

        if product["id"] == product_id:

            return products.pop(index)

    return None

def get_products(db: Session):
    result = db.execute(
        select(Product)
    )

    return result.scalars().all()