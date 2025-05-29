from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.configurations.database import get_db
from src.schemas.category_schema import CreateCategory, CategoryResponse
from src.services.category_service import CategoryService

router = APIRouter()

@router.post("/create", response_model=CategoryResponse)
def create_category(category_data: CreateCategory, db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.create(category_data)


@router.get("/list", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.list_categories()