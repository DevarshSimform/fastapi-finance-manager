from typing import Annotated
from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from src.configurations.database import get_db
from src.schemas.auth_schema import RegisterUser, UserResponse, LoginUser, Token
from src.services.auth_service import AuthService

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: RegisterUser, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.create(user)

@router.post("/login", response_model=Token, deprecated=True)
def login_user(user: Annotated[LoginUser, Form()], db: Session = Depends(get_db)) -> Token:
    service = AuthService(db)
    return service.login_user(user)