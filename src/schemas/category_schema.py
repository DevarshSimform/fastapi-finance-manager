import re
from datetime import datetime
from typing import ClassVar

from pydantic import BaseModel, field_validator


class BaseCategory(BaseModel):
    name: str


class CreateCategory(BaseCategory):

    pattern: ClassVar[str] = r"^[a-z0-9\- ]{3,50}$"

    @field_validator("name", mode="before")
    def improve_category_name(cls, value):
        print("-----------in field validator mode = before")
        return re.sub(r"\s+", " ", value.strip()).lower()

    @field_validator("name")
    def validate_name(cls, value):
        print("-------------in validate-name", value)
        if not re.fullmatch(cls.pattern, value):
            raise ValueError(
                "Category name must be 3 to 50 characters long, and only include lowercase letters, numbers, dashes, and single spaces."
            )
        return value


class CategoryDetail(BaseCategory):
    id: int

    class Config:
        from_attributes = True


class CategoryResponse(BaseCategory):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        json_encoders = {datetime: lambda value: value.strftime("%Y-%m-%d %H:%M:%S")}
