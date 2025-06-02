from fastapi import HTTPException

from src.repositories.category_repo import CategoryRepository
from src.repositories.transaction_repo import TransactionRepository
from src.schemas.transaction_schema import TransactionDetail


class TransactionService:
    def __init__(self, db):
        self.transaction_repo = TransactionRepository(db)
        self.category_repo = CategoryRepository(db)

    def create(self, user_id, data):
        category = self.category_repo.get_category_by_id(data.category_id)
        if not category.user_id == user_id:
            raise HTTPException(
                detail="You can only use your categories", status_code=400
            )
        return self.transaction_repo.create(user_id, data)

    def list_transactions(self, current_user_id):
        return self.transaction_repo.get_transactions(current_user_id)

    def get_transaction(self, current_user_id, transaction_id):
        transaction = self.transaction_repo.get_transaction_by_id(
            current_user_id, transaction_id
        )
        if not transaction:
            raise HTTPException(detail="Transaction not found", status_code=404)
        return TransactionDetail.from_orm(transaction)

    def update_transaction(self, current_user_id, transaction_id, new_data):
        if not self.transaction_repo.is_exist_by_id(current_user_id, transaction_id):
            raise HTTPException(detail="Transaction not found", status_code=404)
        return self.transaction_repo.update_transaction(
            current_user_id, transaction_id, new_data
        )
        # return {"message": "Transaction updated"}

    def delete_transaction(self, current_user_id, transaction_id):
        if not self.transaction_repo.is_exist_by_id(current_user_id, transaction_id):
            raise HTTPException(detail="Transaction not found", status_code=404)
        self.transaction_repo.soft_delete_transaction_by_id(
            current_user_id, transaction_id
        )
        return {"message": "Transaction deleted"}
