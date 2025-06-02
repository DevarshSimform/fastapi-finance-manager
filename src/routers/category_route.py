from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.dependences.auth_dependency import get_current_user_with_db
from src.schemas.auth_schema import UserFullResponse
from src.schemas.category_schema import CategoryResponse, CreateCategory
from src.services.category_service import CategoryService

router = APIRouter()


@router.post("/create", response_model=CategoryResponse)
def create_category(
    category_data: CreateCategory,
    user_with_db: tuple[UserFullResponse, Session] = Depends(get_current_user_with_db),
):
    user, db = user_with_db
    service = CategoryService(db)
    return service.create(user.id, category_data)


@router.get("/list", response_model=list[CategoryResponse])
def get_categories(
    user_with_db: tuple[UserFullResponse, Session] = Depends(get_current_user_with_db),
):
    user, db = user_with_db
    service = CategoryService(db)
    return service.list_categories(user.id)


@router.get("/{id}", response_model=CategoryResponse)
def get_category(
    id: int,
    user_with_db: tuple[UserFullResponse, Session] = Depends(get_current_user_with_db),
):
    user, db = user_with_db
    service = CategoryService(db)
    return service.get_category(user.id, id)


@router.patch("/update/{id}", response_model=CategoryResponse)
def update_category(
    id: int,
    user_with_db: tuple[UserFullResponse, Session] = Depends(get_current_user_with_db),
    name: str = Query(...),
):
    user, db = user_with_db
    service = CategoryService(db)
    return service.update_category_name(user.id, id, name)


@router.delete("/delete/{id}")
def delete_category(
    id: int,
    user_with_db: tuple[UserFullResponse, Session] = Depends(get_current_user_with_db),
):
    user, db = user_with_db[1]
    service = CategoryService(db)
    return service.delete_category(user.id, id)
