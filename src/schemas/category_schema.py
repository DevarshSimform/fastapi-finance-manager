from datetime import datetime

from pydantic import BaseModel


class BaseCategory(BaseModel):
    name: str


class CreateCategory(BaseCategory):
    pass
    # user_id: int


class CategoryResponse(BaseCategory):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        json_encoders = {datetime: lambda value: value.strftime("%Y-%m-%d %H:%M:%S")}
