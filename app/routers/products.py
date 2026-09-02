
from fastapi import APIRouter, Depends, status,HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.product import (
    ProductResponse,
    CreateProduct
)
from app.services.product_service import (
    get_products,
    create_product,
    get_product_by_id
)


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get(
    "/",
    response_model=list[ProductResponse]
)
def read_products(
    db: Session = Depends(get_db)
):
    return get_products(db)


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product_endpoint(
    product: CreateProduct,
    db: Session = Depends(get_db)
):
    return create_product(db, product)


@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def read_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = get_product_by_id(
        db,
        product_id
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product