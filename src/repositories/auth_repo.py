from sqlalchemy.orm import Session

from src.models.user_model import User
from src.schemas.auth_schema import RegisterUser, UserResponse


class AuthRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, user_data: RegisterUser) -> UserResponse:
        user = User(
            **user_data.model_dump(exclude={'password', 'confirm_password'}),
            password_hash = user_data.confirm_password,
            is_active = False
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def is_user_exist(self, email):
        return True if self.db.query(User.email).filter_by(email = email).first() else False
    
    def get_user_by_email(self, email):
        return self.db.query(User).filter_by(email=email).first()