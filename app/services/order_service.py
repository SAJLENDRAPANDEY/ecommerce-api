from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem
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
    order_items_data = []

    # ---------------------------------------------
    # Validate cart and calculate total
    # ---------------------------------------------

    for product_id, quantity in user_cart.items():

        product = db.get(Product, product_id)

        if product is None:
            return None

        if product.stock < quantity:
            return None

        subtotal = product.price * quantity
        total_amount += subtotal

        order_items_data.append({
            "product": product,
            "quantity": quantity,
            "price": product.price
        })

    # ---------------------------------------------
    # Create Order
    # ---------------------------------------------

    order = Order(
        user_id=user_id,
        total_amount=total_amount,
        status="pending"
    )

    db.add(order)
    db.flush()

    # ---------------------------------------------
    # Create Order Items
    # ---------------------------------------------

    for item in order_items_data:

        order_item = OrderItem(
            order_id=order.id,
            product_id=item["product"].id,
            quantity=item["quantity"],
            price=item["price"]
        )

        db.add(order_item)

        # Reduce product stock
        item["product"].stock -= item["quantity"]

    # ---------------------------------------------
    # Save Everything
    # ---------------------------------------------

    db.commit()
    db.refresh(order)

    # Load order items
    order.items

    # Clear cart
    cart_items.pop(user_id, None)

    return order


def get_user_orders(
    db: Session,
    user_id: int
):
    return (
        db.query(Order)
        .filter(
            Order.user_id == user_id
        )
        .order_by(
            Order.created_at.desc()
        )
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