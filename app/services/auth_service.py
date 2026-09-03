from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate


def create_user(
    db: Session,
    user_data: UserCreate
):
    existing_user = db.execute(
        select(User).where(
            User.email == user_data.email
        )
    ).scalar_one_or_none()

    if existing_user:
        return None

    user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hash_password(
            user_data.password
        )
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user