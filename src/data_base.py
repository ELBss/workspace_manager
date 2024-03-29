import psycopg2
from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, literal_column, select
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class UserRole(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    role = Column(String)

def connect_to_db():
    # Подключение к базе данных
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="",
        host="localhost",
        port="5430"
    )

    # Создание курсора
    cur = conn.cursor()
    conn.autocommit = True

    # Выполнение SQL-запроса для проверки существования базы данных
    cur.execute("""
                SELECT 1 
                FROM pg_catalog.pg_database 
                WHERE datname = %s
                """, ("user_auth_db",))

    # Проверка результата запроса
    exists = cur.fetchone()

    if not exists:
        # Выполнение SQL-запроса для создания новой базы данных
        cur.execute("CREATE DATABASE user_auth_db")

    # Закрытие курсора и соединения
    cur.close()
    conn.close()



