import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


# чтение таблица User
class UserRead(BaseModel):
    id: int
    phone: str
    login: str
    name: str
    birth: datetime.date
    tg: str
    email: str

    class Config:
        orm_mode = True


# запись таблица User
class UserBase(BaseModel):
    phone: str = Field(default="7XXXXXXXXXX", description="client's phone number")
    login: str
    name: str
    birth: datetime.datetime
    tg: Optional[str]
    email: Optional[str]


    @validator('phone')  # проверка правильности ввода номера телефона
    def phone_numeric(cls, v):
        if not v.isnumeric() or not v.startswith('7'):
            raise ValueError('must be numeric and starts with 7')
        elif len(v) != 11:
            raise ValueError('must contains 11 nums')
        return v


    class Config:
        orm_mode = True
