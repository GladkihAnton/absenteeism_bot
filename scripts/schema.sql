CREATE SCHEMA "absence";
CREATE TABLE absence.user
(
    telegram_user_id int primary key,
    telegram_chat_id int unique not null,
    name             varchar,
    role_id          int references absence.role (id),
    office_id        int references absence.office (id)
);
CREATE INDEX user_telegram_user_id_ix ON absence.user (telegram_user_id);
CREATE INDEX user_telegram_chat_id_ix ON absence.user (telegram_chat_id);

CREATE TABLE absence.office
(
    id   serial primary key,
    name varchar
);

CREATE TABLE absence.role
(
    id   serial primary key,
    name varchar not null
);

CREATE TABLE absence.absence
(
    id               serial primary key,
    message          varchar,
    date             date,
    telegram_user_id varchar references absence.user (telegram_user_id)
);
CREATE INDEX absence_telegram_user_id ON absence.absence (telegram_user_id);
