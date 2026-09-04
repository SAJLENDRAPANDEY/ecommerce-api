from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.category import Category


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True
    )

    category = relationship(
        "Category",
        back_populates="products"
    )

    order_items = relationship(
    "OrderItem",
    back_populates="product"
    )