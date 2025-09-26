import re
from datetime import datetime
from enum import Enum
from typing import ClassVar, Literal

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


class OAuthProvider(str, Enum):
    GOOGLE = "google"
    # GITHUB = "github"
    # TWITTER = "twitter"


class TokenType(str, Enum):
    ACCESS = "access"
    EMAIL_VERIFICATION = "email_verification"
    BEARER = "bearer"


class UserBase(BaseModel):
    email: EmailStr
    firstname: str
    lastname: str


class RegisterUser(UserBase):
    password: str
    confirm_password: str

    password_regex: ClassVar[str] = (
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    )

    @model_validator(mode="after")
    def match_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Password and Confirm-Password does not match")
        return self

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not re.fullmatch(cls.password_regex, value):
            raise ValueError("Enter valid password")
        return value


class OAuthUser(UserBase):
    """Schema for creating/fetching users via OAuth providers."""

    # OAuth fields
    oauth_provider: Literal["google", "none"]
    oauth_id: str  # e.g., Google "sub" or GitHub "id"

    class Config:
        from_attributes = True


class RegisterResponse(BaseModel):
    message: str


class UserDetail(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    id: int
    # is_admin: bool
    created_at: datetime
    updated_at: datetime | None
    last_login: datetime | None

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda value: value.strftime("%Y-%m-%d %H:%M:%S")}


class LoginUser(BaseModel):
    email: EmailStr = Field(alias="username")
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenOauthResponse(Token):
    user: UserResponse
