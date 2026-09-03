from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user

from app.models.user import User
from app.models.product import Product


router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


# Temporary cart storage
# Later this can be replaced with a proper Cart/CartItem database model.
cart_items: dict[int, dict[int, int]] = {}


# --------------------------------------------------
# Add Product To Cart
# --------------------------------------------------

@router.post(
    "/add/{product_id}",
    status_code=status.HTTP_201_CREATED
)
def add_to_cart(
    product_id: int,
    quantity: int = 1,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than 0"
        )

    product = db.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    if product.stock < quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough stock available"
        )

    user_cart = cart_items.setdefault(
        current_user.id,
        {}
    )

    user_cart[product_id] = (
        user_cart.get(product_id, 0) + quantity
    )

    return {
        "message": "Product added to cart",
        "product_id": product_id,
        "quantity": user_cart[product_id]
    }


# --------------------------------------------------
# Get Cart
# --------------------------------------------------

@router.get("/")
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_cart = cart_items.get(
        current_user.id,
        {}
    )

    items = []
    total = 0

    for product_id, quantity in user_cart.items():

        product = db.get(Product, product_id)

        if product is None:
            continue

        subtotal = product.price * quantity
        total += subtotal

        items.append({
            "product_id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": quantity,
            "subtotal": subtotal
        })

    return {
        "items": items,
        "total": total
    }


# --------------------------------------------------
# Remove Product From Cart
# --------------------------------------------------

@router.delete("/{product_id}")
def remove_from_cart(
    product_id: int,
    current_user: User = Depends(get_current_user)
):
    user_cart = cart_items.get(
        current_user.id,
        {}
    )

    if product_id not in user_cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found in cart"
        )

    del user_cart[product_id]

    return {
        "message": "Product removed from cart"
    }


# --------------------------------------------------
# Clear Cart
# --------------------------------------------------

@router.delete("/")
def clear_cart(
    current_user: User = Depends(get_current_user)
):
    cart_items.pop(
        current_user.id,
        None
    )

    return {
        "message": "Cart cleared successfully"
    }