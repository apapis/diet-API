# app/services/meal_service.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models import Meal, IngredientVariation
from app.schemas.meal import MealCreate, MealUpdate

class MealService:
    def __init__(self, db: Session):
        self.db = db

    def get_meal(self, meal_id: int) -> Optional[Meal]:
        return self.db.query(Meal).filter(Meal.id == meal_id).first()

    def list_meals(self) -> List[Meal]:
        return self.db.query(Meal).all()

    def create_meal(self, meal_data: MealCreate) -> Meal:
        new_meal = Meal(
            meal_type=meal_data.meal_type,
            name=meal_data.name,
            instructions=meal_data.instructions,
            calories=meal_data.calories,
            protein=meal_data.protein,
            fat=meal_data.fat,
            carbs=meal_data.carbs,
        )
        # Dodajemy domyślną wariację składników – etykieta "default"
        new_variation = IngredientVariation(
            variation_label="default",
            ingredients=meal_data.ingredient_variations
        )
        new_meal.ingredient_variations.append(new_variation)
        self.db.add(new_meal)
        self.db.commit()
        self.db.refresh(new_meal)
        return new_meal

    def create_meals(self, meals_data: List[MealCreate]) -> List[Meal]:
        """
        Dodaje wiele przepisów (meals) jednocześnie.
        Wszystkie obiekty są dodawane do sesji, a commit wykonywany jest raz na końcu.
        """
        new_meals = []
        for meal_data in meals_data:
            new_meal = Meal(
                meal_type=meal_data.meal_type,
                name=meal_data.name,
                instructions=meal_data.instructions,
                calories=meal_data.calories,
                protein=meal_data.protein,
                fat=meal_data.fat,
                carbs=meal_data.carbs,
            )
            # Dodajemy domyślną wariację składników
            new_variation = IngredientVariation(
                variation_label="default",
                ingredients=meal_data.ingredient_variations
            )
            new_meal.ingredient_variations.append(new_variation)
            self.db.add(new_meal)
            new_meals.append(new_meal)
        self.db.commit()
        for meal in new_meals:
            self.db.refresh(meal)
        return new_meals

    def update_meal(self, meal_id: int, meal_data: MealUpdate) -> Optional[Meal]:
        meal = self.get_meal(meal_id)
        if not meal:
            return None
        meal.meal_type = meal_data.meal_type
        meal.name = meal_data.name
        meal.instructions = meal_data.instructions
        meal.calories = meal_data.calories
        meal.protein = meal_data.protein
        meal.fat = meal_data.fat
        meal.carbs = meal_data.carbs

        if meal_data.ingredient_variations is not None:
            if meal.ingredient_variations:
                meal.ingredient_variations[0].ingredients = meal_data.ingredient_variations
            else:
                new_variation = IngredientVariation(
                    variation_label="default",
                    ingredients=meal_data.ingredient_variations
                )
                meal.ingredient_variations.append(new_variation)

        self.db.commit()
        self.db.refresh(meal)
        return meal

    def delete_meal(self, meal_id: int) -> bool:
        meal = self.get_meal(meal_id)
        if not meal:
            return False
        self.db.delete(meal)
        self.db.commit()
        return True
