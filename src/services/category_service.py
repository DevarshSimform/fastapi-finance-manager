from fastapi import HTTPException

from src.repositories.category_repo import CategoryRepository


class CategoryService:
    def __init__(self, db):
        self.category_repo = CategoryRepository(db)

    def create(self, user_id, data):
        if self.category_repo.is_exist_by_name(data.name):
            raise HTTPException(
                detail="Category with this name already exists", status_code=400
            )
        return self.category_repo.create(user_id, data)

    def list_categories(self, current_user_id):
        return self.category_repo.get_categories(current_user_id)

    def get_category(self, current_user_id, category_id):
        category = self.category_repo.get_category_by_id(category_id)
        if not category.user_id == current_user_id:
            pass
        return category

    def update_category_name(self, current_user_id, category_id, name):
        if not self.category_repo.is_exist_by_id(category_id):
            pass
        return self.category_repo.update_category_name(
            current_user_id, category_id, name
        )

    def delete_category(self, current_user_id, category_id):
        if not self.category_repo.is_exist_by_id(category_id):
            pass
        self.category_repo.soft_delete_category_by_id(current_user_id, category_id)
        return {"message": "Category deleted"}
