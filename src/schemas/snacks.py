from datetime import datetime
from decimal import Decimal
from typing import List, Self
from uuid import UUID

from pydantic import BaseModel, Field

from db_models.snacks import Pizza
from schemas.shared import GenericOrmBasedSchema


class PizzaFilter(BaseModel):
    name__icontains: str | None = Field(None, alias="name")
    ingredients__id: UUID | None = Field(None, alias="ingredient")


class PizzaIngredientOut(GenericOrmBasedSchema):
    id: UUID
    name: str


class PizzaOut(GenericOrmBasedSchema):
    id: UUID
    name: str
    price: Decimal
    ingredients: List[PizzaIngredientOut]
    images: List[str]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, pizza: Pizza) -> Self:
        return PizzaOut(
            id=pizza.id,
            name=pizza.name,
            price=pizza.price,
            ingredients=[
                PizzaIngredientOut(id=ingredient.id, name=ingredient.name)
                for ingredient in pizza.ingredients
            ],
            images=pizza.images,
            created_at=pizza.created_at,
            updated_at=pizza.updated_at,
        )


class PizzaExtraOut(GenericOrmBasedSchema):
    id: UUID
    name: str
    price: Decimal
