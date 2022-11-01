from fastapi import FastAPI, Depends, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas import User, UserCreate
from app.crud import get_user, get_user_by_phone, create_user
from app.database import SessionLocal,engine
from app.exceptions import PhoneExistsException


description = """
Система управления ресурсами

REST API
проект Акселератора SkillFactory (Тестовое задание)

## Методы
POST/v1/auth/register - принимает JSON с данными пользователя
GET/v1/user/{id} - возвращает JSON со всеми полями пользователя

"""

app = FastAPI(
    title="Resource Managment System REST API",
    description=description,
)


# Dependency (database session)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"documentation": "/docs"}


# регистрация нового пользователя
@app.post(
    "/v1/auth/register/",
    response_model=UserCreate,
    description='Принимает JSON',
    name="Добавить пользователя",
    status_code=201,
)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_phone(db, phone=data.phone)
    if db_user:
        raise PhoneExistsException(data.phone)
    else:
        user = create_user(db, user=data)

    return JSONResponse(
        status_code=201,
        content={"id": user.id}
    )

# возвращает json с идентификатором пользователя
@app.post(
    "/v1/auth/login/",
    response_model=User,
    name="Json с id пользователя",
    description="принимает JSON с логином и паролем",
)
def login_user(login: str, password: str, db: Session = Depends(get_db)):
    pass


# получить данные user по id.
@app.get(
    "/v1/user/{id}/",
    response_model=User,
    name="Получить данные о пользователе по id",
    description="возвращает json со всеми полями пользователя (кроме пароля)",
)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = get_user(db, id=id)
    if not user:
        return JSONResponse(
            status_code=404,
            content={"message": "Пользователь не найден"}
        )
    return user


# Обработчики исключений
@app.exception_handler(PhoneExistsException)
async def phone_exists_handler(request: Request, exc: PhoneExistsException):
    return JSONResponse(
        status_code=400,
        content={"code": "400", "message": "User с таким номером телефона уже существует"}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    for i in exc.errors():
        error = i.get("msg")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"code": "422", "message": error},
    )

