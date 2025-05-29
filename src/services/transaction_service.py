from sqlalchemy.orm import Session

from src.repositories.transaction_repo import TransactionRepository


class TransactionService:

    def __init__(self, db):
        self.transaction_repo = TransactionRepository(db)

    def create(self, data):
        return self.transaction_repo.create(data)

    def list_transactions(self):
        return self.transaction_repo.get_transactions()