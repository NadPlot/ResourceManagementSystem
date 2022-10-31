from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.database import User
from app.schemas import UserCreate


# получить user по id
def get_user(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()


# регистрация user
def create_user(db: Session, user: UserCreate):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# получить user по номеру телефона
# (для проверки есть ли уже такой номер в БД)
def get_user_by_phone(db: Session, phone: int):
    return db.query(User).filter(User.phone == phone).first()

# получить id по логину и паролю
def get_user_id(db: Session, login: str, password: str):
    db_login = db.query(User).filter(User.login == login).first
