# ResourceManagementSystem
SkillFactory Accelerator project (test task)

### Тестовое задание - Система управления Ресурсами
Задача: реализовать REST API с тремя http-методами:
1) POST /v1/auth/register - принимает JSON
2) POST /v1/auth/login - принимает JSON(логин, пароль)
3) GET /v1/user - возвращает JSON со всеми полями пользователя

Для реализации API использован FastAPI

СУБД - PostgreSQL

SQL script для создания схемы БД: postgres.sql

### Запустить проект
Скопировать код из репозитория (git clone).
Построить и запустить контейнер docker (FastApi + PostgreSQL):

    $ docker-compose up -d --build

Проект будет запущен локально на http://127.0.0.1:8008/

Документация: http://127.0.0.1:8008/docs

Cкрипт postgres.sql - будет выполнен при запуске контейнера docker,
будет создана таблица БД "User" с одной строкой (user id=1)

Проверить, что таблица создана:
    

    $ docker-compose exec db psql --username=postgres --dbname==postgres
    # \c postgres
    # \dt



### Подключение к БД
Для проекта в docker-compose.yml был добавлен service db (PostgreSQL).
Данные БД для подключения указаны в переменной окружения DATABASE_URL
и в переменных POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB.

В файле config.py определены переменные для конкретной среды,
db_url будет автоматически загружен из переменной окружения DATABASE_URL.
В database.py для создания engine загружается db_url.

#### Реализованы http-методы:
1) POST /v1/auth/register - принимает JSON:



    {
      "phone": "+79167003020",
      "login": "rubella19",
      "password": "1Qwerty!",
      "name": "Анастасия",
      "birth": "2000-07-28",
      "tg": "@Rubella19",
      "email": "anastasia.a.krasnova@gmail.com"
    }

Пример запроса: GET/v1/auth/register/   201 Created

Пример вывода:


    {"id": "2"}

В случае, если возраст менее 18, будет сообщение об ошибке:


    {
      "code": "422",
      "message": "Your age must be 18+"
    }


В случае ошибки, например если номер уже существует:

    {
      "code": "400",
      "message": "User с таким номером телефона уже существует"
    }


Если номер введен некорректно (содержит буквы, начинается не с "+7"),
сообщение об ошибке:


    {
      "code": "422",
      "message": "phone must be numeric"
    }


2) POST /v1/auth/login - принимает json с логином паролем и возвращает
json с идентификатором пользователя в случае успеха,


    {
      "id": 1
    }


в случае ошибки возвращает json, например:


    {
      "code": 400,
      "message": "Неправильный пароль"
    }



3) GET /v1/user
с query-параметром id, возвращает json со всеми полями пользователя
(кроме пароля) и Код-Текст ошибки

Пример запроса: GET/v1/user/1/  200 OK

Пример вывода:

    {
      "phone": "+79167003020",
      "login": "rubella19",
      "name": "Анастасия",
      "birth": "2000-07-28",
      "tg": "@Rubella19",
      "email": "anastasia.a.krasnova@gmail.com",
      "id": 1
     }

Если пользователь с id не найден:
Пример запроса: GET/v1/user/2/  404 Not Found

Пример вывода:

    {
      "message": "Пользователь не найден"
    }

### Запуск тестов


    $ docker-compose exec web pytest
