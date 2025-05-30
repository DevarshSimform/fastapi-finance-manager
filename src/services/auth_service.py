from sqlalchemy.orm import Session

from src.repositories.auth_repo import AuthRepository
from src.utils.auth_util import create_access_token
from src.schemas.auth_schema import Token, LoginUser


class AuthService:

    def __init__(self, db: Session):
        self.auth_repo = AuthRepository(db)

    def create(self, user_data):
        if self.auth_repo.is_user_exist(user_data.email):
            pass
        return self.auth_repo.create(user_data)
    
    def login_user(self, user: LoginUser) -> Token:
        user = self.auth_repo.authenticate_user(user)
        if not user:
            pass
        access_token = create_access_token(data={"sub": user.email})
        return Token(
            access_token=access_token, token_type="bearer"
        )