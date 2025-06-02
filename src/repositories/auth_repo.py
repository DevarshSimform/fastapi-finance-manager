from datetime import datetime

from sqlalchemy.orm import Session

from src.models.user_model import User
from src.schemas.auth_schema import LoginUser, RegisterUser, UserResponse
from src.utils.auth_util import get_password_hash, verify_password


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_data: RegisterUser) -> UserResponse:
        user = User(
            **user_data.model_dump(exclude={"password", "confirm_password"}),
            password_hash=get_password_hash(user_data.confirm_password),
            is_active=False,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def is_user_exist(self, email):
        return (
            True if self.db.query(User.email).filter_by(email=email).first() else False
        )

    def get_user_by_email(self, email):
        return self.db.query(User).filter_by(email=email).first()

    def authenticate_user(self, user_login: LoginUser):
        user = self.db.query(User).filter_by(email=user_login.email).first()
        if not user or not verify_password(user_login.password, user.password_hash):
            return False
        user.last_login = datetime.now()
        self.db.commit()
        return user

    def is_user_inactive(self, email):
        return (
            True
            if self.db.query(User.email).filter(
                User.email == email, User.is_active is False
            )
            else False
        )

    def activate_user(self, email):
        user = self.get_user_by_email(email)
        user.is_active = True
        self.db.commit()
