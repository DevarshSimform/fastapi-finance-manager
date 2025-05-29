from enum import Enum as PyEnum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship

from src.configurations.database import Base


class SourceEnum(str, PyEnum):
    cash = "cash"
    card = "card"
    bank_payment = "bank_payment"

class TypeEnum(str, PyEnum):
    income = "income"
    expense = "expense"


class Transaction(Base):

    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    source = Column(SQLEnum(SourceEnum, name="source_enum"), nullable=False)
    type = Column(SQLEnum(TypeEnum, name="type_enum"), nullable=False)

    amount = Column(Float)
    is_deleted = Column(Boolean, default=False, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=None, onupdate=datetime.now())
    created_at = Column(DateTime(timezone=True), default=datetime.now())

    # Relationships
    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")