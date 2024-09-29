DROP TABLE IF EXISTS users, managers;

CREATE TABLE users(
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(20) UNIQUE NOT NULL,
    password VARCHAR(60) NOT NULL
);

CREATE TABLE managers(
    login VARCHAR(20) PRIMARY KEY,
    password VARCHAR(60) NOT NULL
)