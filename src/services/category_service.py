from sqlalchemy.orm import Session

from src.repositories.category_repo import CategoryRepository


class CategoryService:

    def __init__(self, db):
        self.category_repo = CategoryRepository(db)

    def create(self, data):
        if self.category_repo.is_exist_by_name(data.name):
            pass
        return self.category_repo.create(data)
    
    def list_categories(self):
        return self.category_repo.get_categories()