from fastapi import FastAPI
from app.api.endpoints import recipes

app = FastAPI()

# Rejestracja routerów
app.include_router(recipes.router, prefix="/recipes", tags=["recipes"])

@app.get("/")
def root():
    return {"message": "Welcome to the Recipe API"}
