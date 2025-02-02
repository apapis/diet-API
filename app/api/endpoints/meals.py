# app/api/endpoints/meals.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import SessionLocal
from app.schemas.meal import MealCreate, MealUpdate, MealOut
from app.services.meal_service import MealService

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_meal_service(db: Session = Depends(get_db)) -> MealService:
    return MealService(db)

@router.get("/", response_model=List[MealOut])
def list_meals(service: MealService = Depends(get_meal_service)):
    return service.list_meals()

@router.get("/{meal_id}", response_model=MealOut)
def get_meal(meal_id: int, service: MealService = Depends(get_meal_service)):
    meal = service.get_meal(meal_id)
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    return meal

@router.post("/", response_model=MealOut)
def create_meal(meal_data: MealCreate, service: MealService = Depends(get_meal_service)):
    return service.create_meal(meal_data)

@router.post("/bulk", response_model=List[MealOut])
def create_meals_bulk(meals_data: List[MealCreate], service: MealService = Depends(get_meal_service)):
    """
    Endpoint, który umożliwia dodanie wielu przepisów naraz.
    Przykładowe dane wejściowe to lista obiektów typu MealCreate.
    """
    created_meals = service.create_meals(meals_data)
    if not created_meals:
        raise HTTPException(status_code=400, detail="No meals were created")
    return created_meals

@router.put("/{meal_id}", response_model=MealOut)
def update_meal(meal_id: int, meal_data: MealUpdate, service: MealService = Depends(get_meal_service)):
    updated_meal = service.update_meal(meal_id, meal_data)
    if not updated_meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    return updated_meal

@router.delete("/{meal_id}")
def delete_meal(meal_id: int, service: MealService = Depends(get_meal_service)):
    result = service.delete_meal(meal_id)
    if not result:
        raise HTTPException(status_code=404, detail="Meal not found")
    return {"message": "Meal deleted successfully"}
