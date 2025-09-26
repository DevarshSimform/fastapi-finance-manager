from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.configurations.database import get_db
from src.repositories.auth_repo import AuthRepository
from src.schemas.auth_schema import Token, UserResponse
from src.utils.auth_util import get_access_payload
from src.utils.logger import logger

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user_with_db(
    token: Annotated[Token, Depends(oauth2_schema)], db: Session = Depends(get_db)
) -> tuple[UserResponse, Session]:
    """
    Dependency to get the currently authenticated user along with DB session.

    Raises:
        HTTPException: If token is invalid, expired, user does not exist, or is inactive.

    Returns:
        tuple[UserResponse, Session]: Authenticated user schema and DB session.
    """
    try:
        payload = get_access_payload(token)
    except HTTPException as e:
        logger.warning(f"Access token invalid: {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        ) from e

    email: str = payload.get("sub")
    if not email:
        logger.warning("Access token missing 'sub' field")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
        )

    auth_repo = AuthRepository(db)
    user = auth_repo.get_user_by_email(email)
    if not user:
        logger.warning(f"User not found for email: {email}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if not user.is_active:
        logger.warning(f"Inactive user attempted access: {email}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive"
        )

    user_schema = UserResponse.from_orm(user)
    logger.info(f"Authenticated user: {email}")

    return user_schema, db
