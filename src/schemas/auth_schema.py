from datetime import datetime
from pydantic import BaseModel, EmailStr



class UserBase(BaseModel):
    
    email: EmailStr
    username: str
    firstname: str
    lastname: str


class RegisterUser(UserBase):

    password: str
    confirm_password: str


class UserResponse(UserBase):

    id: int
    # is_admin: bool
    created_at: datetime
    updated_at: datetime | None
    last_login: datetime | None

    class Config:
        json_encoders = {
            datetime: lambda value: value.strftime("%Y-%m-%d %H:%M:%S")
        }