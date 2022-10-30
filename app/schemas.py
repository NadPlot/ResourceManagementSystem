import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator, EmailStr


# База чтение и запись, таблица User
class UserBase(BaseModel):
    phone: str = Field(default="+7XXXXXXXXXX", description="user's phone number")
    login: str
    name: str
    birth: datetime.date
    tg: Optional[str]
    email: Optional[EmailStr]
    
    @validator('phone')  # проверка правильности ввода номера телефона
    def phone_numeric(cls, v):
        if not v.startswith('+7'):
            raise ValueError('must be numeric and starts with +7')
        elif len(v) != 12:
            raise ValueError('must contains +7 and 11 nums')
        return v


# запись таблица User
class UserCreate(UserBase):
    password: str


# чтение таблица User:
class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True
