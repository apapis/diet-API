from sqlalchemy.orm import Session
from app.db.models import Meal, IngredientVariation

def save_meals_to_db(db: Session, recipes: list):
    """
    Dla każdego przepisu w liście:
      - Jeśli przepis (na podstawie meal_type i recipe_name) już istnieje, dodajemy do niego nową wariację składników.
      - W przeciwnym razie tworzymy nowy przepis (Meal) i przypisujemy do niego wariację składników.
      
    Każdy przepis z PDF (dostarczony jako słownik) powinien mieć strukturę np.:
    
    {
      "meal_type": "breakfast",
      "recipe_name": "Słodki omlet kokosowy z bananem i jagodami",
      "ingredients": [
          {"name": "Jajo kurze", "quantity": "150 g", "measure": "3 średnie sztuki"},
          {"name": "Mąka kokosowa", "quantity": "50 g", "measure": "50 g"}
      ],
      "instructions": [
          "W misce roztrzepać jajka z mąką kokosową, napojem i szczyptą soli, aż masa będzie jednolita.",
          "Na rozgrzaną patelnię z oliwą wylać masę jajeczną.",
          "Na wierzchu ułożyć plasterki banana i jagody."
      ],
      "calories": 695,
      "protein": 29,
      "fat": 36,
      "carbs": 66,
      # opcjonalnie: "variation_label": "wersja z większą ilością jajek"
    }
    """
    saved_meals = []

    for recipe in recipes:
        # Wyszukujemy istniejący przepis na podstawie meal_type i recipe_name
        existing_meal = (
            db.query(Meal)
            .filter(
                Meal.meal_type == recipe["meal_type"],
                Meal.name == recipe["recipe_name"]
            )
            .first()
        )

        if existing_meal:
            # Jeśli przepis istnieje, dodajemy nową wariację składników
            new_variation = IngredientVariation(
                variation_label=recipe.get("variation_label", "default"),
                ingredients=recipe["ingredients"]
            )
            existing_meal.ingredient_variations.append(new_variation)
            db.add(new_variation)
            saved_meals.append(existing_meal)
        else:
            # Jeśli przepis nie istnieje, tworzymy nowy rekord przepisu i dodajemy wariację składników
            new_meal = Meal(
                meal_type=recipe["meal_type"],
                name=recipe["recipe_name"],
                instructions=recipe["instructions"],
                calories=recipe.get("calories"),
                protein=recipe.get("protein"),
                fat=recipe.get("fat"),
                carbs=recipe.get("carbs"),
            )
            new_variation = IngredientVariation(
                variation_label=recipe.get("variation_label", "default"),
                ingredients=recipe["ingredients"]
            )
            new_meal.ingredient_variations.append(new_variation)
            db.add(new_meal)
            saved_meals.append(new_meal)

    db.commit()

    # Odświeżamy rekordy, aby mieć dostęp do wygenerowanych identyfikatorów i relacji
    for meal in saved_meals:
        db.refresh(meal)

    return saved_meals
