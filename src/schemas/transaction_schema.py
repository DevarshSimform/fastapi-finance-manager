import re
from datetime import datetime

from pydantic import BaseModel, model_validator

from src.models.transaction_model import SourceEnum, TypeEnum
from src.schemas.auth_schema import UserDetail
from src.schemas.category_schema import CategoryDetail


class BaseTransaction(BaseModel):
    source: SourceEnum
    type: TypeEnum
    amount: float
    description: str
    category_id: int


class CreateTransaction(BaseTransaction):

    @model_validator(mode="after")
    def normalize_fields(self):
        # Trim, reduce multiple spaces to single space, and lowercase
        self.description = re.sub(r"\s+", " ", self.description.strip()).lower()

        # Normalize amount based on transaction type
        if self.type == TypeEnum.EXPENSE:
            self.amount = -abs(self.amount)
        else:
            self.amount = abs(self.amount)
        return self


class TransactionListResponse(BaseTransaction):
    id: int
    user_id: int


class TransactionResponse(BaseTransaction):
    id: int
    user_id: int
    updated_at: datetime | None
    created_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda value: value.strftime("%Y-%m-%d %H:%M:%S"),
        }


class TransactionDetail(BaseTransaction):
    id: int
    user: UserDetail
    category: CategoryDetail
    updated_at: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda value: value.strftime("%Y-%m-%d %H:%M:%S"),
        }


class TransactionUpdate(BaseTransaction):
    source: SourceEnum | None
    type: TypeEnum | None
    amount: float | None
    description: str | None
    category_id: int | None

    @model_validator(mode="after")
    def to_lowercase(self):
        # Ensure description is lowercase
        self.description = self.description.lower()

        # Normalize amount based on transaction type
        if self.type == TypeEnum.EXPENSE:
            self.amount = -abs(self.amount)
        else:
            self.amount = abs(self.amount)
        return self
