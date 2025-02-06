from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from app.api.endpoints import process, meals  # Dołączamy moduł meals
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

# Dodaj middleware CORS
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dodajemy endpointy z process
app.include_router(process.router, prefix="/process", tags=["process"])
# Dodajemy endpointy z meals
app.include_router(meals.router, prefix="/meals", tags=["meals"])

@app.get("/")
def root():
    return {"message": "Hello to the Recipe API"}
