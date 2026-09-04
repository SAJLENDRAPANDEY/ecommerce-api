from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user

from app.models.user import User

from app.schemas.order import OrderResponse

from app.services.order_service import (
    create_order,
    get_user_orders,
    get_order_by_id
)


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


# --------------------------------------------------
# Checkout / Create Order
# --------------------------------------------------

@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED
)
def checkout(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = create_order(
        db,
        current_user.id
    )

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty or product stock is insufficient"
        )

    return order


# --------------------------------------------------
# Get My Orders
# --------------------------------------------------

@router.get(
    "/",
    response_model=list[OrderResponse]
)
def read_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_orders(
        db,
        current_user.id
    )


# --------------------------------------------------
# Get Order By ID
# --------------------------------------------------

@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def read_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = get_order_by_id(
        db,
        order_id,
        current_user.id
    )

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    return order