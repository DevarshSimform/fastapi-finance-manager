from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.dependences.auth_dependency import get_current_user_with_db
from src.schemas.auth_schema import UserResponse
from src.schemas.transaction_schema import (
    CreateTransaction,
    TransactionDetail,
    TransactionListResponse,
    TransactionResponse,
    TransactionUpdate,
)
from src.services.transaction_service import TransactionService

router = APIRouter()


@router.post("/create", response_model=TransactionResponse)
def create_transaction(
    transaction_data: CreateTransaction,
    user_with_db: tuple[UserResponse, Session] = Depends(get_current_user_with_db),
):
    user, db = user_with_db
    service = TransactionService(db)
    return service.create(user.id, transaction_data)


@router.get("/list", response_model=list[TransactionListResponse])
def list_transactions(
    user_with_db: tuple[UserResponse, Session] = Depends(get_current_user_with_db),
):
    user, db = user_with_db
    service = TransactionService(db)
    return service.list_transactions(user.id)


@router.get(
    "/{id}", response_model=TransactionDetail, response_model_exclude=["category_id"]
)
def get_transaction(
    id: int,
    user_with_db: tuple[UserResponse, Session] = Depends(get_current_user_with_db),
):
    user, db = user_with_db
    service = TransactionService(db)
    return service.get_transaction(user.id, id)


@router.patch("/{id}", response_model=TransactionResponse)
def update_transaction(
    id: int,
    data: TransactionUpdate,
    user_with_db: tuple[UserResponse, Session] = Depends(get_current_user_with_db),
):
    user, db = user_with_db
    service = TransactionService(db)
    return service.update_transaction(user.id, id, data)


@router.delete("/{id}")
def delete_transaction(
    id: int,
    user_with_db: tuple[UserResponse, Session] = Depends(get_current_user_with_db),
):
    user, db = user_with_db
    service = TransactionService(db)
    return service.delete_transaction(user.id, id)
