from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from tenacity import retry, stop_after_attempt, wait_fixed
import os
from dotenv import load_dotenv
from sqlalchemy.sql import text

# Załaduj zmienne środowiskowe
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Utwórz silnik bazy danych
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Funkcja do sprawdzania połączenia z bazą
@retry(stop=stop_after_attempt(10), wait=wait_fixed(2))
def check_db_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))  # Użyj text() dla zapytania SQL
    except Exception as e:
        print("Baza danych nie jest jeszcze gotowa, próbuję ponownie...")
        raise e
