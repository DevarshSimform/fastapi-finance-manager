from typing import Annotated

from fastapi import APIRouter, Depends, Form, Query, Request
from sqlalchemy.orm import Session

from src.configurations.database import get_db
from src.dependences.auth_dependency import get_current_user_with_db
from src.schemas.auth_schema import (
    LoginUser,
    RegisterUser,
    Token,
    UserFullResponse,
    UserResponse,
)
from src.services.auth_service import AuthService

router = APIRouter()


@router.post("/register")
def register_user(user: RegisterUser, request: Request, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.create(user, request)


@router.post("/login", response_model=Token, deprecated=True)
def login_user(
    user: Annotated[LoginUser, Form()], db: Session = Depends(get_db)
) -> Token:
    service = AuthService(db)
    return service.login_user(user)


@router.get("/verify-email", name="verify_email")
def verify_email(token: str = Query(...), db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.verify_user(token)


@router.get("/profile", response_model=UserResponse)
def get_user_profile(
    user_with_db: tuple[UserFullResponse, Session] = Depends(get_current_user_with_db),
):
    user, db = user_with_db
    service = AuthService(db)
    print("--------email------------", user.email)
    return service.get_profile(user.email)
