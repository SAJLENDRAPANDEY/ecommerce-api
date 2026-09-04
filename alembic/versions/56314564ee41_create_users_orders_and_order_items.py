"""create users orders and order items

Revision ID: 56314564ee41
Revises: 64f984e9fbe3
Create Date: 2026-09-05 00:45:32.095692
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "56314564ee41"
down_revision: Union[str, Sequence[str], None] = "64f984e9fbe3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    op.create_index(
        "ix_users_id",
        "users",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_users_email",
        "users",
        ["email"],
        unique=True,
    )

    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("total_amount", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_orders_id",
        "orders",
        ["id"],
        unique=False,
    )

    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["orders.id"],
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_order_items_id",
        "order_items",
        ["id"],
        unique=False,
    )


def downgrade() -> None:

    op.drop_index("ix_order_items_id", table_name="order_items")
    op.drop_table("order_items")

    op.drop_index("ix_orders_id", table_name="orders")
    op.drop_table("orders")

    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")