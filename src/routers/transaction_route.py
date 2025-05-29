from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from src.configurations.database import get_db
from src.schemas.transaction_schema import CreateTransaction, TransactionResponse
from src.services.transaction_service import TransactionService

router = APIRouter()


@router.post("/create", response_model=TransactionResponse)
def create_transaction(transaction_data: CreateTransaction, db: Session = Depends(get_db)):
    service = TransactionService(db)
    return service.create(transaction_data)


@router.get("/list", response_model=list[TransactionResponse])
def list_transactions(db: Session = Depends(get_db)):
    service = TransactionService(db)
    return service.list_transactions()