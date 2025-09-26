from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext

from src.configurations.settings import settings
from src.schemas.auth_schema import TokenType

EMAIL_SECRET_KEY = settings.EMAIL_SECRET_KEY
ACCESS_TOKEN = settings.GENERAL_SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
EMAIL_TOKEN_EXPIRE_MINUTES = settings.EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """Verify a stored password against one provided by user"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Hash a password for storing."""
    return pwd_context.hash(password)


def generate_token(
    data: dict,
    expires_delta,
    token_type: str,
    secret_key: str,
    algorithm: str = ALGORITHM,
):
    """Generate a JWT token with an expiration time and type."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    to_encode.update(
        {
            "exp": expire,
            "type": token_type,
        }
    )
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def get_payload(
    token: str,
    expected_type: str,
    secret_key: str,
    algorithm: str = ALGORITHM,
) -> dict:
    """Decode JWT token and validate its type."""
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    # validate token type
    token_type = payload.get("type")
    if token_type != expected_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid token type. Expected {expected_type}, got {token_type}",
        )
    return payload


def get_email_payload(
    token: str,
) -> dict:
    """Decode JWT email verification token."""
    return get_payload(
        token,
        expected_type=TokenType.EMAIL_VERIFICATION,
        secret_key=EMAIL_SECRET_KEY,
    )


def get_access_payload(
    token: str,
) -> dict:
    """Decode JWT access token."""
    return get_payload(
        token,
        expected_type=TokenType.ACCESS,
        secret_key=ACCESS_TOKEN,
    )


def create_email_token(data: dict):
    """Create a JWT token for email verification."""
    return generate_token(
        data,
        expires_delta=EMAIL_TOKEN_EXPIRE_MINUTES,
        token_type=TokenType.EMAIL_VERIFICATION,
        secret_key=EMAIL_SECRET_KEY,
    )


def create_access_token(data: dict):
    """Create a JWT access token."""
    return generate_token(
        data,
        expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES,
        token_type=TokenType.ACCESS,
        secret_key=ACCESS_TOKEN,
    )
