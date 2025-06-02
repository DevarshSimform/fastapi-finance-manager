import re
from datetime import datetime
from typing import ClassVar

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


class UserBase(BaseModel):
    email: EmailStr
    username: str
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
    def validate_password(cls, value):
        if not re.fullmatch(cls.password_regex, value):
            raise ValueError("Enter valid password")
        return value


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
        json_encoders = {datetime: lambda value: value.strftime("%Y-%m-%d %H:%M:%S")}


class UserFullResponse(UserResponse):
    is_admin: bool


class LoginUser(BaseModel):
    email: EmailStr = Field(alias="username")
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
