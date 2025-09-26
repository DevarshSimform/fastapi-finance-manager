from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session

from src.configurations.oauth.google import google
from src.configurations.settings import settings
from src.repositories.auth_repo import AuthRepository
from src.schemas.auth_schema import (
    LoginUser,
    RegisterResponse,
    Token,
    TokenOauthResponse,
    TokenType,
    UserResponse,
)
from src.utils.auth_util import (
    create_access_token,
    create_email_token,
    get_email_payload,
)
from src.utils.email_util import send_verification_email_task
from src.utils.logger import logger
from src.utils.oauth_parser import parse_google_userinfo


class AuthService:
    """Service Layer for authentication-related operations."""

    def __init__(self, db: Session):
        self.auth_repo = AuthRepository(db)

    async def create(self, user_data):
        """Create a new user and send email verification."""
        existing_user = self.auth_repo.get_user_by_email(user_data.email)

        if existing_user:
            # Case 1: user already has password → block
            if existing_user.password_hash:
                logger.warning(
                    f"Attempt to create a user that already exists with password: {user_data.email}"
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User already exists",
                )

            # Case 2: user exists but password is None (Google login user)
            logger.info(
                f"User {user_data.email} exists with Google login. Allowing password setup."
            )

            # Update the existing user with the password
            self.auth_repo.update_password(existing_user.id, user_data.password)

            # If user is already active (via Google login), no verification needed
            if existing_user.is_active:
                return RegisterResponse(
                    message="Password set successfully. You can now log in with email and password."
                )

            # Fallback: if somehow inactive, send verification email
            email_token = create_email_token(data={"sub": user_data.email})
            data = {
                "verification_url": f"{settings.BASE_URL}/api/auth/verify-email/?token={email_token}",
                "username": f"{existing_user.firstname} {existing_user.lastname}",
            }
            send_verification_email_task.delay(user_data.email, data)
            logger.info(f"Verification email sent again for {user_data.email}")

            return RegisterResponse(
                message="Password set. Please check your email to verify your account."
            )

        # Case 3: brand new user
        self.auth_repo.create(user_data)
        logger.info(f"New user created: {user_data.email}")

        email_token = create_email_token(data={"sub": user_data.email})
        logger.info(
            f"Email verification token generated for {user_data.email}: {email_token}"
        )

        data = {
            "verification_url": f"{settings.BASE_URL}/api/auth/verify-email/?token={email_token}",
            "username": f"{user_data.firstname} {user_data.lastname}",
        }

        send_verification_email_task.delay(user_data.email, data)
        logger.info(f"Verification email task queued for {user_data.email}")

        return RegisterResponse(
            message="User created. Please check your email to verify your account."
        )

    async def oauth_google(self, request: Request):
        """
        Handle OAuth2 Google login.
        """
        redirect_uri = f"{settings.BASE_URL}/api/auth/callback/google"
        return await google.authorize_redirect(request, redirect_uri)

    async def oauth_google_callback(self, request: Request):
        """
        Handle OAuth2 Google login callback.
        """
        try:
            token = await google.authorize_access_token(request)
            logger.info("OAuth token received from Google")
        except Exception as e:
            logger.error(f"Failed to authorize Google token: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Google token authorization failed",
            ) from e

        if "userinfo" not in token:
            logger.warning("No userinfo found in OAuth token")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No userinfo in token response",
            )

        try:
            user_info = token["userinfo"]
            logger.info(f"User-info = {user_info}")
        except Exception as e:
            logger.error(f"Failed to parse user info: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"User info parsing failed: {e}",
            ) from e

        user_data = parse_google_userinfo(user_info)
        logger.info(f"Parsed OAuth user data: {user_data}")

        # Pass validated object to repo
        user = self.auth_repo.create_oauth_user(user_data)

        # Generate token
        access_token = create_access_token({"sub": user.email, "type": "access"})
        logger.info(f"User {user.email} authenticated via Google")

        return TokenOauthResponse(
            access_token=access_token,
            token_type=TokenType.BEARER,
            user=UserResponse.from_orm(user),
        )

    def login_user(self, login_data: LoginUser) -> Token:
        """
        Authenticate and log in a user.

        Raises HTTPException if credentials are invalid or user is inactive.
        Returns a JWT access token on successful login.
        """
        user = self.auth_repo.authenticate_user(login_data)

        if not user:
            logger.warning(f"Failed login attempt for email: {login_data.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not user.is_active:
            logger.warning(f"Inactive user login attempt: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive. Please verify your email.",
            )

        access_token = create_access_token(data={"sub": user.email})
        logger.info(f"User logged in successfully: {user.email}")

        return Token(access_token=access_token, token_type=TokenType.BEARER)

    def verify_user(self, token):
        """
        Verify a user's email using the provided token.

        Raises HTTPException if token is invalid, expired, or user not found.
        Returns success message if user is activated.
        """
        try:
            payload = get_email_payload(token)
        except HTTPException as e:
            logger.warning(f"Email verification failed: {e.detail}")
            raise HTTPException(
                status_code=e.status_code,
                detail=f"Email verification failed: {e.detail}",
            ) from e
        email: str = payload.get("sub")
        if not email:
            logger.error("Token payload missing email (sub)")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token payload missing email (sub)",
            )

        user = self.auth_repo.get_user_by_email(email)
        if not user:
            logger.warning(f"Attempt to verify non-existent user: {email}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
            )

        if user.is_active:
            logger.info(f"User already verified: {email}")
            return {"message": "User is already verified"}

        # Activate user
        self.auth_repo.activate_user(email)
        logger.info(f"User successfully verified: {email}")

        return {"message": "User is verified and active now"}

    def get_profile(self, email: str) -> UserResponse:
        """
        Fetch a user's profile by email.

        Raises HTTPException if user does not exist.
        Returns a serialized UserResponse.
        """
        user = self.auth_repo.get_user_by_email(email)

        if not user:
            logger.warning(f"Attempt to access profile for non-existent email: {email}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        logger.info(f"User profile accessed: {email}")

        # Convert ORM object to schema for API response
        return UserResponse.from_orm(user)
