from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.configurations.database import get_db
from src.schemas.auth_schema import UserFullResponse
from src.schemas.category_schema import CreateCategory, CategoryResponse
from src.services.category_service import CategoryService
from src.dependences.auth_dependency import get_current_user_with_db

router = APIRouter()

@router.post("/create", response_model=CategoryResponse)
def create_category(category_data: CreateCategory, user_with_db: tuple[UserFullResponse, Session] = Depends(get_current_user_with_db)):
    user, db = user_with_db
    service = CategoryService(db)
    return service.create(user.id, category_data)


@router.get("/list", response_model=list[CategoryResponse])
def get_categories(user_with_db: tuple[UserFullResponse, Session] = Depends(get_current_user_with_db)):
    user, db = user_with_db
    service = CategoryService(db)
    return service.list_categories()