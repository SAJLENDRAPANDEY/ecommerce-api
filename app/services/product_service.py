
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import CreateProduct


def get_products(db: Session):
    result = db.execute(
        select(Product)
    )

    return result.scalars().all()


def create_product(db: Session, product_data: CreateProduct):
    product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def get_product_by_id(db: Session, product_id: int):
    result = db.execute(
        select(Product).where(Product.id == product_id)
    )

    return result.scalar_one_or_none()