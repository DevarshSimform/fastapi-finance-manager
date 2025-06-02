from datetime import datetime

from pydantic import BaseModel

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
    pass


class TransactionListResponse(BaseTransaction):
    id: int
    user_id: int


class TransactionResponse(BaseTransaction):
    id: int
    user_id: int
    updated_at: datetime | None
    created_at: datetime
    # amount: float

    class Config:
        json_encoders = {
            datetime: lambda value: value.strftime("%Y-%m-%d %H:%M:%S"),
            # Decimal: lambda v: format(v, '.2f')
        }


class TransactionDetail(BaseTransaction):
    id: int
    user: UserDetail
    category: CategoryDetail
    updated_at: datetime | None
    created_at: datetime
    # amount: float

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda value: value.strftime("%Y-%m-%d %H:%M:%S"),
        }


class TransactionUpdate(BaseModel):
    source: SourceEnum | None
    type: TypeEnum | None
    amount: float | None
    description: str | None
    category_id: int | None
