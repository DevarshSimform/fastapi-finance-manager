from src.models.transaction_model import Transaction
from src.schemas.transaction_schema import CreateTransaction, TransactionResponse


class TransactionRepository:
    def __init__(self, db):
        self.db = db

    def create(self, user_id, data: CreateTransaction) -> TransactionResponse:
        transaction = Transaction(
            **data.model_dump(exclude={"category_id"}),
            user_id=user_id,
            category_id=data.category_id,
        )
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def get_transactions(self):
        transactions = self.db.query(Transaction).filter(
            Transaction.is_deleted is False
        )
        return transactions
