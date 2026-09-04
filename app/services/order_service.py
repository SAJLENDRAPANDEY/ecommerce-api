from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.product import Product

from app.routers.cart import cart_items


def create_order(
    db: Session,
    user_id: int
):
    user_cart = cart_items.get(user_id)

    if not user_cart:
        return None

    total_amount = 0

    # Check products and stock
    for product_id, quantity in user_cart.items():

        product = db.get(Product, product_id)

        if product is None:
            return None

        if product.stock < quantity:
            return None

        total_amount += product.price * quantity

    # Create order
    order = Order(
        user_id=user_id,
        total_amount=total_amount,
        status="pending"
    )

    db.add(order)

    # Reduce stock
    for product_id, quantity in user_cart.items():

        product = db.get(Product, product_id)

        product.stock -= quantity

    db.commit()
    db.refresh(order)

    # Clear cart after successful order
    cart_items.pop(user_id, None)

    return order


def get_user_orders(
    db: Session,
    user_id: int
):
    return (
        db.query(Order)
        .filter(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
        .all()
    )


def get_order_by_id(
    db: Session,
    order_id: int,
    user_id: int
):
    return (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.user_id == user_id
        )
        .first()
    )