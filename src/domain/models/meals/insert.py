from uuid import UUID

from pydantic import Field

from src.config.validation import FieldValidator


class MealInsertModel(FieldValidator):
    meal_id: UUID
    user_id: UUID
    meal_name: str = Field(min_length=3)
    calories: float = Field(gt=0)

    class Config:
        frozen = True
