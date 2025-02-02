from fastapi import FastAPI
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from app.api.endpoints import recipes, meals  # Dołączamy moduł meals
from app.db.init_db import init_db
from app.db.session import check_db_connection

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    # Logika przy starcie aplikacji
    check_db_connection()
    init_db()
    yield
    # Logika przy zamykaniu aplikacji (jeśli potrzebna)
    print("Shutting down application...")

app = FastAPI(lifespan=lifespan)

# Dodajemy endpointy z recipes
app.include_router(recipes.router, prefix="/recipes", tags=["recipes"])
# Dodajemy endpointy z meals
app.include_router(meals.router, prefix="/meals", tags=["meals"])

@app.get("/")
def root():
    return {"message": "Hello to the Recipe API"}
