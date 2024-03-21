from _decimal import Decimal
from datetime import datetime
from typing import List, Self
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from starlette import status

from db_models.snacks import Pizza
from deps import get_pizzas_service
from error_codes import UserSnackErrorCode
from schemas import Pagination, PaginatedUserSnackResponse
from services.pizzas_service import PizzasService

router = APIRouter()


class PizzaFilter(BaseModel):
    name__icontains: str | None = Field(None, alias="name")
    ingredients__id: UUID | None = Field(None, alias="ingredient")


class PizzaIngredientOut(BaseModel):
    id: UUID
    name: str


class PizzaOut(BaseModel):
    id: UUID
    name: str
    ingredients: List[PizzaIngredientOut]
    images: List[str]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_pizza(cls, pizza: Pizza) -> Self:
        return PizzaOut(
            id=pizza.id,
            name=pizza.name,
            ingredients=[
                PizzaIngredientOut(
                    id=ingredient.id,
                    name=ingredient.name
                ) for ingredient in pizza.ingredients
            ],
            images=pizza.images,
            created_at=pizza.created_at,
            updated_at=pizza.updated_at
        )


@router.get(
    "",
    response_model=PaginatedUserSnackResponse[PizzaOut],
    status_code=status.HTTP_200_OK,
    summary="Fetch and search through Pizzas"
)
async def get_pizzas(
    pizza_service: PizzasService = Depends(get_pizzas_service),
    pagination: Pagination = Depends(),
    pizza_filter: PizzaFilter = Depends()
) -> PaginatedUserSnackResponse[PizzaOut]:
    """
    **Query Filters:**
    - `name`: Finds Pizzas with keyword specified in name.
    """
    pizzas, count = await pizza_service.get_pizzas(pagination, pizza_filter)
    results = [PizzaOut.from_pizza(pizza) for pizza in pizzas]
    return PaginatedUserSnackResponse(
        results=results,
        size=count,
        **pagination.model_dump()
    )


@router.get(
    "/{_id}",
    response_model=PizzaOut,
    status_code=status.HTTP_200_OK,
    summary="Get single Pizza by ID",
    responses={404: {"code": UserSnackErrorCode.NOT_FOUND}}
)
async def get_pizza(
    _id: UUID,
    pizza_service: PizzasService = Depends(get_pizzas_service),
) -> PizzaOut:
    pizza = await pizza_service.get_pizza(_id)
    return PizzaOut.from_pizza(pizza)


class PizzaExtraOut(BaseModel):
    id: UUID
    name: str
    price: Decimal


@router.get(
    "/{_id}/extras",
    response_model=PaginatedUserSnackResponse[PizzaExtraOut],
    status_code=status.HTTP_200_OK,
    summary="Fetch Pizza Extras"
)
async def get_pizza_extras(
    _id: UUID,
    pizza_service: PizzasService = Depends(get_pizzas_service),
    pagination: Pagination = Depends(),
) -> PaginatedUserSnackResponse[PizzaExtraOut]:
    pizza_extras, count = await pizza_service.get_pizza_extras(_id, pagination)

    results = []
    for extra in pizza_extras:
        results.append(
            PizzaExtraOut(
                id=extra.id,
                name=extra.name,
                price=extra.price
            )
        )

    return PaginatedUserSnackResponse(
        results=results,
        size=count,
        **pagination.model_dump()
    )
