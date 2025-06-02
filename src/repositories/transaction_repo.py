from sqlalchemy.orm import joinedload

from src.models.transaction_model import Transaction
from src.schemas.transaction_schema import CreateTransaction, TransactionResponse


class TransactionRepository:
    def __init__(self, db):
        self.db = db

    def create(self, user_id, data: CreateTransaction) -> TransactionResponse:
        # transaction = Transaction(
        #     **data.model_dump(exclude={"category_id"}),
        #     user_id=user_id,
        #     category_id=data.category_id,
        # )
        # self.db.add(transaction)
        # self.db.commit()
        # self.db.refresh(transaction)
        transaction = self.get_transaction_by_id(1)
        return transaction

    def get_transactions(self, current_user_id):
        transactions = self.db.query(Transaction).filter(
            Transaction.is_deleted.is_(False), Transaction.user_id == current_user_id
        )
        return transactions

    def is_exist_by_id(self, current_user_id, transaction_id):
        return (
            True
            if self.db.query(Transaction.id, Transaction.is_deleted).filter(
                Transaction.id == transaction_id,
                Transaction.user_id == current_user_id,
                Transaction.is_deleted.is_(False),
            )
            else False
        )

    def get_transaction_by_id(self, current_user_id, transaction_id):
        return (
            self.db.query(Transaction)
            .options(joinedload(Transaction.user))
            .options(joinedload(Transaction.category))
            .filter(
                Transaction.id == transaction_id,
                Transaction.user_id == current_user_id,
                Transaction.is_deleted.is_(False),
            )
            .first()
        )

    def update_transaction(self, current_user_id, transaction_id, new_data):
        transaction = self.get_transaction_by_id(current_user_id, transaction_id)
        data = new_data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(transaction, key, value)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def soft_delete_transaction_by_id(self, current_user_id, transaction_id):
        transaction = self.get_transaction_by_id(transaction_id)
        if not transaction.user_id == current_user_id:
            pass
        transaction.is_deleted = True
        self.db.commit()
