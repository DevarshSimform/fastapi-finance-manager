from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from src.configurations.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    password_hash = Column(String, nullable=True)

    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)

    is_active = Column(Boolean, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    # OAuth fields
    oauth_provider = Column(
        String, default="none", nullable=False
    )  # 'none', 'google', etc.
    oauth_id = Column(String, nullable=True)  # e.g., Google sub

    created_at = Column(DateTime(timezone=True), default=datetime.now())
    updated_at = Column(DateTime(timezone=True), default=None, onupdate=datetime.now())
    last_login = Column(DateTime(timezone=True), default=None, onupdate=datetime.now())

    # Relationship to transactions
    transactions = relationship("Transaction", back_populates="user")

    @property
    def fullname(self):
        """Return full name as 'Firstname Lastname'"""
        return f"{self.firstname} {self.lastname}"

    @classmethod
    def filter_not_deleted(cls, db):
        """Return query for users that are not soft-deleted."""
        return db.query(cls).filter(cls.is_deleted.is_(False))
