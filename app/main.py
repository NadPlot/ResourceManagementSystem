from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas import UserRead
from app.crud import get_user
from app.database import SessionLocal,engine


description = """
Система управления ресурсами

REST API
проект Акселератора SkillFactory (Тестовое задание)

## Методы
POST/v1/auth/register - принимает JSON
GET/v1/user/{id} - возвращает JSON со всеми полями пользователя

"""

app = FastAPI(
    title="Resource Managment System REST API",
    description=description,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {
    "method GET User by id": "/v1/user/{id} - возвращает json со всеми полями пользователя",
    }


# получить данные user по id.
@app.get(
    "/v1/user/{id}/",
    response_model=UserRead,
    name="Получить данные о пользователе по id",
    description="возвращает json со всеми полями пользователя (кроме пароля)",
)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = get_user(db, id=id)
    if not user:
        return JSONResponse(
            status_code=404,
            content={"message": "Пользователь не найден", "id": f"{id}"}
        )
    return user
