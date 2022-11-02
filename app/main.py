from fastapi import FastAPI, Depends, Request, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

from app.schemas import User, UserCreate, UserLogin, UserId
from app.crud import get_user, create_user, get_user_by_login
from app.database import SessionLocal, engine
from app.exceptions import LoginExistsException


description = """
Система управления ресурсами

REST API
проект Акселератора SkillFactory (Тестовое задание)

## Методы
POST/v1/auth/register - принимает JSON с данными пользователя
POST /v1/auth/login - принимает JSON с логином и паролем
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


# регистрация нового пользователя (password is not hashed)
@app.post(
    "/v1/auth/register/",
    response_model=UserCreate,
    description='Принимает JSON',
    name="Добавить пользователя",
    status_code=201,
)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, user=data)
    return JSONResponse(
        status_code=201,
        content={"id": user.id}
    )


# возвращает json с идентификатором пользователя
@app.post(
    "/v1/auth/login/",
    response_model=UserId,
    name="возвращает json с идентификатором пользователя",
    description="принимает JSON с логином и паролем",
)
def login_user(data: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_login(db, login=data.login)
    if not user:
        raise LoginExistsException(data.login)

    if user.password != data.password:
        return JSONResponse(
            status_code=400,
            content={"code": 400, "message": "Неправильный пароль"}
        )
    return user


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
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    for i in exc.errors():
        error = i.get("msg")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"code": "422", "message": error},
    )


@app.exception_handler(IntegrityError)
async def validation_exception_handler(request, exc: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"code": "422", "message": "User с таким номером телефона уже существует"},
    )


@app.exception_handler(LoginExistsException)
async def login_exists_handler(request: Request, exc: LoginExistsException):
    return JSONResponse(
        status_code=404,
        content={"status": 404, "message": "Пользователь с таким логином не найден"}
    )

