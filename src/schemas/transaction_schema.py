from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, field_validator, model_validator

from src.models.transaction_model import SourceEnum, TypeEnum


class BaseTransaction(BaseModel):

    category_id: int
    source: SourceEnum
    type : TypeEnum
    amount: float

    # @model_validator(mode='before')
    # def float_to_decimal(self):
    #     return round(Decimal(self.amount), 2)


class CreateTransaction(BaseTransaction):
    pass


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