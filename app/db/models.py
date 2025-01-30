from sqlalchemy import Column, Integer, String, JSON
from app.db.session import Base

class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    meal_type = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False)
    ingredients = Column(JSON, nullable=False)
    instructions = Column(JSON, nullable=False)
    calories = Column(Integer, nullable=True)
    protein = Column(Integer, nullable=True)
    fat = Column(Integer, nullable=True)
    carbs = Column(Integer, nullable=True)
    