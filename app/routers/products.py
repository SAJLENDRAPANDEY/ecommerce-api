from fastapi import APIRouter, HTTPException, status

from app.schemas.product import (
    ProductResponse,
    CreateProduct,
    ProductUpdate
)

from app.services.product_service import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product
)


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get(
    "/",
    response_model=list[ProductResponse]
)
def get_products():

    return get_all_products()


@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product(product_id: int):

    product = get_product_by_id(product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product_endpoint(product: CreateProduct):

    return create_product(product)


@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product_endpoint(
    product_id: int,
    product: ProductUpdate
):

    updated_product = update_product(
        product_id,
        product
    )

    if updated_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return updated_product


@router.delete(
    "/{product_id}"
)
def delete_product_endpoint(product_id: int):

    deleted_product = delete_product(product_id)

    if deleted_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return {
        "message": "Product deleted successfully"
    }

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.product_service import get_products


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/", response_model=list[ProductResponse])
def read_products(
    db: Session = Depends(get_db)
):
    return get_products(db)