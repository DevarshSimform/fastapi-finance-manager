from sqlalchemy.orm import Session

from src.repositories.auth_repo import AuthRepository
from src.schemas.auth_schema import LoginUser, Token
from src.utils.auth_util import create_access_token, create_email_token, get_payload
from src.utils.email_util import send_verification_email_task


class AuthService:
    def __init__(self, db: Session):
        self.auth_repo = AuthRepository(db)

    async def create(self, user_data):
        if self.auth_repo.is_user_exist(user_data.email):
            return {"message": "User already exists"}
        self.auth_repo.create(user_data)
        email_token = create_email_token(data={"sub": user_data.email})
        print(email_token)
        data = {
            "verification_url": f"http://localhost:8000/api/auth/verify-email/?token={email_token}",
            "username": user_data.username,
        }
        send_verification_email_task.delay("pateldc014@gmail.com", data)

        return {
            "message": "User created. Please check your email to verify your account."
        }

    def login_user(self, user: LoginUser) -> Token:
        user = self.auth_repo.authenticate_user(user)
        if not user:
            return {"message": "User not exists"}
        access_token = create_access_token(data={"sub": user.email})  # nosec
        return Token(access_token=access_token, token_type="bearer")  # nosec

    def verify_user(self, token):
        payload = get_payload(token)
        email: str = payload.get("sub")
        if email is None:
            return {"message": "User token expired login again"}

        if not self.auth_repo.is_user_inactive(email):
            return {"message": "User not exists"}
        self.auth_repo.activate_user(email)
        return {"message": "User is verified and active now"}

    def get_profile(self, email):
        user = self.auth_repo.get_user_by_email(email)
        return user
