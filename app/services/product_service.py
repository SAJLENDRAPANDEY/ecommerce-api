
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import CreateProduct, ProductUpdate


def get_products(
    db: Session,
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    stock_available: bool | None = None
):
    query = select(Product)

    if search:
        query = query.where(
            Product.name.ilike(f"%{search}%")
        )

    if min_price is not None:
        query = query.where(
            Product.price >= min_price
        )

    if max_price is not None:
        query = query.where(
            Product.price <= max_price
        )

    if stock_available is True:
        query = query.where(
            Product.stock > 0
        )

    if stock_available is False:
        query = query.where(
            Product.stock == 0
        )

    result = db.execute(query)

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


def update_product(
    db: Session,
    product_id: int,
    product_data: ProductUpdate
):
    result = db.execute(
        select(Product).where(Product.id == product_id)
    )

    product = result.scalar_one_or_none()

    if product is None:
        return None

    if product_data.name is not None:
        product.name = product_data.name

    if product_data.description is not None:
        product.description = product_data.description

    if product_data.price is not None:
        product.price = product_data.price

    if product_data.stock is not None:
        product.stock = product_data.stock

    db.commit()
    db.refresh(product)

    return product


def delete_product(
    db: Session,
    product_id: int
):
    result = db.execute(
        select(Product).where(Product.id == product_id)
    )

    product = result.scalar_one_or_none()

    if product is None:
        return None

    db.delete(product)
    db.commit()

    return product

    