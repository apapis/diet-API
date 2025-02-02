# app/schemas/meal.py
from typing import List, Optional, Any
from pydantic import BaseModel

class IngredientVariationOut(BaseModel):
    id: int
    variation_label: Optional[str] = None
    ingredients: Any  # Możesz sprecyzować typ np. List[dict], jeśli masz jednolitą strukturę

    class Config:
        orm_mode = True

class MealBase(BaseModel):
    meal_type: str
    name: str
    instructions: List[str]
    calories: Optional[int] = None
    protein: Optional[int] = None
    fat: Optional[int] = None
    carbs: Optional[int] = None

class MealCreate(MealBase):
    ingredient_variations: List[dict]  # Lista wariacji składników; przy tworzeniu przepisów na początku zazwyczaj jedna wariacja

class MealUpdate(MealBase):
    # Dla uproszczenia przyjmujemy, że przy aktualizacji wszystkie pola są wymagane; możesz dodać opcjonalność
    ingredient_variations: Optional[List[dict]] = None

class MealOut(MealBase):
    id: int
    ingredient_variations: List[IngredientVariationOut] = []

    class Config:
        orm_mode = True
