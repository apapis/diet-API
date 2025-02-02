from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    meal_type = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False)
    instructions = Column(JSON, nullable=False)
    calories = Column(Integer, nullable=True)
    protein = Column(Integer, nullable=True)
    fat = Column(Integer, nullable=True)
    carbs = Column(Integer, nullable=True)

    # Relacja 1:N do wariacji składników
    ingredient_variations = relationship(
        "IngredientVariation",
        back_populates="meal",
        cascade="all, delete-orphan"
    )


class IngredientVariation(Base):
    __tablename__ = "ingredient_variations"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("meals.id", ondelete="CASCADE"), nullable=False)
    variation_label = Column(String(100), nullable=True)
    ingredients = Column(JSON, nullable=False)

    meal = relationship("Meal", back_populates="ingredient_variations")
