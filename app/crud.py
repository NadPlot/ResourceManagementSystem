from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.database import User
from app.schemas import UserRead


# получить user по id
def get_user(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()
