
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import CreateProduct, ProductUpdate


def get_products(
    db: Session,
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    stock_available: bool | None = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "id",
    order: str = "asc"
):
    query = select(Product)

    # Search
    if search:
        query = query.where(
            Product.name.ilike(f"%{search}%")
        )

    # Price filters
    if min_price is not None:
        query = query.where(
            Product.price >= min_price
        )

    if max_price is not None:
        query = query.where(
            Product.price <= max_price
        )

    # Stock filter
    if stock_available is True:
        query = query.where(
            Product.stock > 0
        )

    if stock_available is False:
        query = query.where(
            Product.stock == 0
        )

    # Sorting
    allowed_sort_fields = {
        "id": Product.id,
        "name": Product.name,
        "price": Product.price,
        "stock": Product.stock
    }

    sort_column = allowed_sort_fields.get(
        sort_by,
        Product.id
    )

    if order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Pagination
    offset = (page - 1) * limit

    query = query.offset(offset).limit(limit)

    result = db.execute(query)

    return result.scalars().all()


def create_product(db: Session, product_data: CreateProduct):
    product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock,
        category_id=product_data.category_id
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
    product = db.get(Product, product_id)

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

    if product_data.category_id is not None:
        product.category_id = product_data.category_id

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

    