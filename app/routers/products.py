from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user

from app.models.user import User

from app.schemas.product import (
    ProductResponse,
    CreateProduct,
    ProductUpdate
)

from app.services.product_service import (
    get_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product
)


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# --------------------------------------------------
# Get All Products
# --------------------------------------------------

@router.get(
    "/",
    response_model=list[ProductResponse]
)
def read_products(
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    stock_available: bool | None = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db)
):
    return get_products(
        db=db,
        search=search,
        min_price=min_price,
        max_price=max_price,
        stock_available=stock_available,
        page=page,
        limit=limit,
        sort_by=sort_by,
        order=order
    )


# --------------------------------------------------
# Get Product By ID
# --------------------------------------------------

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


# --------------------------------------------------
# Create Product
# --------------------------------------------------

@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product_endpoint(
    product_data: CreateProduct,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_product(
        db,
        product_data
    )


# --------------------------------------------------
# Update Product
# --------------------------------------------------

@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product_endpoint(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = update_product(
        db,
        product_id,
        product_data
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product


# --------------------------------------------------
# Delete Product
# --------------------------------------------------

@router.delete(
    "/{product_id}"
)
def delete_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = delete_product(
        db,
        product_id
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return {
        "message": "Product deleted successfully"
    }