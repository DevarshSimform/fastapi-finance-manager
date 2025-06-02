from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    username: str
    firstname: str
    lastname: str


class RegisterUser(UserBase):
    password: str
    confirm_password: str


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
