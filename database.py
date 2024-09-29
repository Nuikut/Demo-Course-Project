import os
from fastapi import status, HTTPException
import psycopg
from dotenv import load_dotenv
from fastapi import Request
from auth.utils import encode_jwt
import bcrypt

load_dotenv()
conn = psycopg.connect(host="localhost", user=os.getenv("postgres_user"),
                           password=os.getenv("postgres_password"), dbname="postgres")


def select_all():
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM users')
        print(cursor.fetchall())


def create_user(username: str, password: str) -> bool:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE EXISTS (SELECT user_id FROM users WHERE username = %s)", [username])
        if cursor.fetchone():
            return False
        cursor.execute("INSERT INTO users(username, password) VALUES (%s, %s)",
                       [username, bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()])
        conn.commit()
        return True


def validate_user(username: str, password: str):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM users WHERE username = %s', [username])
        data = cursor.fetchone()
        if data and bcrypt.checkpw(password=password.encode(), hashed_password=data[2].encode()):
            return {"access_token": encode_jwt(data)}
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def validate_manager(login: str, password: str):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM managers WHERE login = %s', [login])
        data = cursor.fetchone()
        if data and bcrypt.checkpw(password=password.encode(), hashed_password=data[2].encode()):
            return {"access_token": encode_jwt(data)}
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
