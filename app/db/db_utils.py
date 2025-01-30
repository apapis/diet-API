from sqlalchemy.orm import Session
from app.db.models import Meal

def save_meals_to_db(db: Session, recipes: list):
    """Zapisuje listę przepisów do bazy danych."""
    new_meals = []
    
    for recipe in recipes:
        new_meal = Meal(
            meal_type=recipe["meal_type"],
            name=recipe["recipe_name"],
            ingredients=recipe["ingredients"],
            instructions=recipe["instructions"],  
            calories=recipe.get("calories"),
            protein=recipe.get("protein"),
            fat=recipe.get("fat"),
            carbs=recipe.get("carbs"),
        )
        db.add(new_meal)
        new_meals.append(new_meal)

    db.commit()
    
    for meal in new_meals:
        db.refresh(meal)
    
    return new_meals
