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

Реализованы http-методы:
3) GET /v1/user
с query-параметром id, возвращает json со всеми полями пользователя
(кроме пароля) и Код-Текст ошибки
Пример запроса: GET/v1/user/1/  200 OK
Пример вывода:
    {
  "id": 1,
  "phone": "+79167003020",
  "login": "rubella19",
  "name": "Анастасия",
  "birth": "2000-07-28",
  "tg": "@Rubella19",
  "email": "anastasia.a.krasnova@gmail.com"
}

Если пользователь с id не найден:
Пример запроса: GET/v1/user/2/  404 Not Found
Пример вывода:
    {
  "message": "Пользователь не найден",
  "id": "2"
}

