from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from src.configurations.database import get_db
from src.schemas.auth_schema import UserFullResponse
from src.schemas.transaction_schema import CreateTransaction, TransactionResponse
from src.services.transaction_service import TransactionService
from src.dependences.auth_dependency import get_current_user_with_db

router = APIRouter()


@router.post("/create", response_model=TransactionResponse)
def create_transaction(transaction_data: CreateTransaction, user_with_db: tuple[UserFullResponse, Session] = Depends(get_current_user_with_db)):
    user, db = user_with_db
    service = TransactionService(db)
    return service.create(user.id, transaction_data)


@router.get("/list", response_model=list[TransactionResponse])
def list_transactions(user_with_db: tuple[UserFullResponse, Session] = Depends(get_current_user_with_db)):
    user, db = user_with_db
    service = TransactionService(db)
    return service.list_transactions()