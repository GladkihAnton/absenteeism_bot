CREATE SCHEMA "absence";


CREATE TABLE absence.office
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR
);


CREATE TABLE absence.role
(
    id   serial PRIMARY KEY,
    name VARCHAR NOT NULL
);


CREATE TABLE absence.user
(
    telegram_user_id  INT PRIMARY KEY,
    name              VARCHAR NOT NULL,
    role_id           INT REFERENCES absence.role (id) NOT NULL,
    office_id         INT REFERENCES absence.office (id) NOT NULL,
    active            BOOLEAN DEFAULT FALSE NOT NULL
);


CREATE TABLE absence.absence
(
    id               serial primary key,
    message          VARCHAR NOT NULL,
    date             DATE NOT NULL,
    telegram_user_id INT REFERENCES absence.user (telegram_user_id) NOT NULL
);
CREATE INDEX absence_telegram_user_id ON absence.absence (telegram_user_id);
