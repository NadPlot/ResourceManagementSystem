from sqlalchemy.orm import Session
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


# получить user по логину
def get_user_by_login(db: Session, login: str):
    return db.query(User).filter(User.login == login).first()

