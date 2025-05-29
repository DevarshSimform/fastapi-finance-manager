from sqlalchemy.orm import Session

from src.models.category_model import Category
from src.schemas.category_schema import CreateCategory, CategoryResponse

class CategoryRepository:

    def __init__(self, db):
        self.db = db

    def create(self, data: CreateCategory) -> CategoryResponse:
        category = Category(
            **data.model_dump(),
            user_id = 1         # Will change this hardcoded when add login
        )
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def is_exist_by_name(self, name):
        return True if self.db.query(Category.name).filter_by(name = name).first() else False
    
    def get_categories(self):
        categories = self.db.query(Category).filter(Category.is_deleted == False)
        return categories