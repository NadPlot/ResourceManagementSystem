CREATE SEQUENCE IF NOT EXISTS user_id_seq;

CREATE TABLE "public"."User"(
    "id" int4 NOT NULL DEFAULT nextval('user_id_seq'::regclass),
    "phone" varchar,
    "login" varchar(80),
    "password" varchar,
    "name" varchar(80),
    "birth" date,
    "tg" varchar,
    "email" varchar(80),
    PRIMARY KEY ("id"),
    CONSTRAINT email_unique UNIQUE ("email")
);

INSERT INTO "public"."User" (
    "phone",
    "login",
    "password",
    "name",
    "birth",
    "tg",
    "email"
)
    VALUES (
    '+79167003020',
    'rubella19',
    '1Qwerty!',
    'Анастасия',
    '2000-07-28',
    '@Rubella19',
    'anastasia.a.krasnova@gmail.com'
);

SELECT * FROM "public"."User";

