import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


class Database:
    conn = psycopg.connect(host="localhost", user=os.getenv("postgres_user"),
                               password=os.getenv("postgres_password"), dbname="postgres")

    def select_all(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users')
        print(cursor.fetchall())

    def create_user(self, username:str, password:str) -> None:
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO users(username, password) VALUES (%s, %s) ON CONFLICT (username) DO NOTHING", [username, password])
        self.conn.commit()
