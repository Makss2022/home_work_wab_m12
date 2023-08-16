from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    name: str = Field(max_length=50, min_length=3)
    surname: str = Field(max_length=50, min_length=3)
    email: EmailStr
    phone: str = Field('+380501234567', max_length=13, min_length=10)
    birthday: date
    notes: str = Field(min_length=3)


class ContactResponse(ContactModel):
    id: int = 1
    
    class Config:
        orm_mode = True


...


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
