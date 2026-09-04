from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OrderItemResponse(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int
    subtotal: float


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    created_at: datetime
    items: list[OrderItemResponse] = []

    model_config = ConfigDict(
        from_attributes=True
    )