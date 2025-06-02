from src.models.category_model import Category
from src.schemas.category_schema import CategoryResponse, CreateCategory


class CategoryRepository:
    def __init__(self, db):
        self.db = db

    def create(self, user_id, data: CreateCategory) -> CategoryResponse:
        category = Category(**data.model_dump(), user_id=user_id)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def is_exist_by_name(self, name):
        return (
            True
            if self.db.query(Category.name)
            .filter(Category.name == name, Category.is_deleted.is_(False))
            .first()
            else False
        )

    def get_categories(self, current_user_id):
        categories = self.db.query(Category).filter(
            Category.is_deleted.is_(False), Category.user_id == current_user_id
        )
        return categories

    def is_exist_by_id(self, category_id):
        return (
            True
            if self.db.query(Category.id, Category.is_deleted)
            .filter(Category.id == category_id, Category.is_deleted.is_(False))
            .first()
            else False
        )

    def get_category_by_id(self, category_id):
        return (
            self.db.query(Category)
            .filter(Category.id == category_id, Category.is_deleted.is_(False))
            .first()
        )

    def update_category_name(self, current_user_id, category_id, name):
        category = self.get_category_by_id(category_id)
        if not category.user_id == current_user_id:
            pass
        category.name = name
        self.db.commit()
        return category

    def soft_delete_category_by_id(self, current_user_id, category_id):
        category = self.get_category_by_id(category_id)
        if not category.user_id == current_user_id:
            pass
        category.is_deleted = True
        self.db.commit()
