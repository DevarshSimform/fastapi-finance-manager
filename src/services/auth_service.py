from sqlalchemy.orm import Session

from src.repositories.auth_repo import AuthRepository
from src.schemas.auth_schema import LoginUser, Token
from src.utils.auth_util import create_access_token, create_email_token, get_payload


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
        access_token = create_access_token(data={"sub": user.email})  # nosec
        return Token(access_token=access_token, token_type="bearer")  # nosec

    def create_demo(self, user_data):
        if self.auth_repo.is_user_exist(user_data.email):
            pass
        # create user here
        email_token = create_email_token(data={"sub": user_data.email})
        print(email_token)
        # send mail here
        return {"msg": "User created. Please check your email to verify your account."}

    def verify(self, token):
        payload = get_payload(token)
        email = payload.get("sub")

        payload: str = get_payload(token)
        if email is None:
            pass
        # self.auth_repo
