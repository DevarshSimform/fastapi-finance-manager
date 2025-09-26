from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.models.user_model import User
from src.schemas.auth_schema import LoginUser, OAuthUser, RegisterUser, UserResponse
from src.utils.auth_util import get_password_hash, verify_password
from src.utils.logger import logger


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_data: RegisterUser) -> UserResponse:
        """Create a new user in the database."""
        user = User(
            **user_data.model_dump(exclude={"password", "confirm_password"}),
            password_hash=get_password_hash(user_data.password),
            is_active=False,
        )
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to create user: {e}")
            raise

    def create_oauth_user(self, user_data: OAuthUser) -> User:
        """
        Create a new user with OAuth credentials.
        If the email already exists, attach oauth_provider/oauth_id.
        """
        try:
            # Check if user already exists
            user = self.db.query(User).filter(User.email == user_data.email).first()

            if user:
                # If the user exists but not linked to this provider yet
                if user.oauth_provider == "none" or not user.oauth_id:
                    user.oauth_provider = user_data.provider
                    user.oauth_id = user_data.provider_id
                    self.db.commit()
                    self.db.refresh(user)
                return user

            # Otherwise, create a new OAuth user
            new_user = User(
                email=user_data.email,
                firstname=user_data.firstname,
                lastname=user_data.lastname,
                password_hash=None,
                is_active=True,  # OAuth users are verified via provider
                is_deleted=False,
                oauth_provider=user_data.oauth_provider,
                oauth_id=user_data.oauth_id,
            )

            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)

            return new_user

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Failed to create OAuth user: {e}")
            raise

    def update_password(self, existing_user_id: int, new_password: str):
        """Update the password for an existing user."""
        user = self.db.query(User).filter(User.id == existing_user_id).first()
        user.password_hash = get_password_hash(new_password)
        self.db.commit()
        self.db.refresh(user)
        return user

    def is_user_exist(self, email):
        # return (
        #     True
        #     if self.db.query(User.email)
        #     .filter(User.email == email, User.is_active.is_(True))
        #     .first()
        #     else False
        # )
        return (
            True
            if User.filter_not_deleted(self.db).filter(User.email == email).first()
            else False
        )

    def get_user_by_email(self, email):
        # return (
        #     self.db.query(User)
        #     .filter(User.email == email, User.is_active.is_(True))
        #     .first()
        # )
        return User.filter_not_deleted(self.db).filter(User.email == email).first()

    def get_raw_user_by_email(self, email):
        return self.db.query(User).filter(User.email == email).first()

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
                User.email == email, User.is_active.is_(False)
            )
            else False
        )

    def activate_user(self, email):
        user = self.get_raw_user_by_email(email)
        user.is_active = True
        self.db.commit()
