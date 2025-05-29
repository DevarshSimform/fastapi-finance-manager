from sqlalchemy.orm import Session
from src.repositories.auth_repo import AuthRepository


class AuthService:

    def __init__(self, db: Session):
        self.auth_repo = AuthRepository(db)

    def create(self, user_data):
        if self.auth_repo.is_user_exist(user_data.email):
            pass
        return self.auth_repo.create(user_data)