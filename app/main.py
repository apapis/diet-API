from fastapi import FastAPI
from app.api.endpoints import recipes
from app.db.init_db import init_db
from app.db.session import check_db_connection

app = FastAPI()

@app.on_event("startup")
def startup():
    # Poczekaj, aż baza danych będzie gotowa
    check_db_connection()
    # Zainicjalizuj bazę danych
    init_db()

app.include_router(recipes.router, prefix="/recipes", tags=["recipes"])

@app.get("/")
def root():
    return {"message": "Hello to the Recipe API"}
