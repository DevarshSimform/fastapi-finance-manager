from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.configurations.database import get_db
from src.schemas.auth_schema import RegisterUser, UserResponse
from src.services.auth_service import AuthService

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: RegisterUser, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.create(user)
