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

    @validator('birth') # проверка возраста (18+)
    def birth_adult(cls, v):
        year_now = datetime.date.today().year
        year_birth = v.year
        delta = year_now - year_birth
        if delta < 18:
            raise ValueError('Your age must be 18+')
        return v
    
    @validator('phone')  # проверка правильности ввода номера телефона
    def phone_numeric(cls, v):
        if not v.startswith('+7'):
            raise ValueError('phone must starts with +7')
        num = v.split('+')[1]
        if not num.isnumeric():
            raise ValueError('phone must be numeric')
        elif len(num) != 11:
            raise ValueError('phone must contains 11 nums')
        return v


# запись таблица User
class UserCreate(UserBase):
    password: str


# чтение таблица User полностью
class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True


# Логин и пароль только (POST /v1/auth/login)
class UserLogin(BaseModel):
    login: str
    password: str


# чтение только id
class UserId(BaseModel):
    id: int
    
    class Config:
        orm_mode = True
