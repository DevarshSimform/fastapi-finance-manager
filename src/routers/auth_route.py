from typing import Annotated

from fastapi import APIRouter, Depends, Form, Query, Request
from sqlalchemy.orm import Session

from src.configurations.database import get_db
from src.dependences.auth_dependency import get_current_user_with_db
from src.schemas.auth_schema import (
    LoginUser,
    RegisterResponse,
    RegisterUser,
    Token,
    UserResponse,
)
from src.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=RegisterResponse, status_code=201)
async def register_user(user: RegisterUser, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    service = AuthService(db)
    return await service.create(user)


# OAuth Routes
@router.get("/oauth/google")
async def oauth_google(request: Request, db: Session = Depends(get_db)):
    """
    OAuth2 Google login.
    """
    service = AuthService(db)
    return await service.oauth_google(request)


@router.get("/callback/google", response_model=Token)
async def oauth_google_callback(request: Request, db: Session = Depends(get_db)):
    """
    OAuth2 Google login callback.
    """
    service = AuthService(db)
    return await service.oauth_google_callback(request)


@router.post("/login", response_model=Token)
def login_user(
    user: Annotated[LoginUser, Form()], db: Session = Depends(get_db)
) -> Token:
    """
    Authenticate user and return JWT token.
    """
    service = AuthService(db)
    return service.login_user(user)


@router.get("/verify-email")
def verify_email(token: str = Query(...), db: Session = Depends(get_db)):
    """
    Verify user's email using token.
    """
    service = AuthService(db)
    return service.verify_user(token)


@router.get("/profile", response_model=UserResponse)
def get_user_profile(
    user_with_db: tuple[UserResponse, Session] = Depends(get_current_user_with_db),
):
    """
    Get current user's profile.
    """
    user, db = user_with_db
    service = AuthService(db)
    return service.get_profile(user.email)
