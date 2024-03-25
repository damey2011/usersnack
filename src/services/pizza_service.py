from typing import List, Tuple
from uuid import UUID

from pydantic import BaseModel
from tortoise.exceptions import DoesNotExist

from db_models.snacks import Pizza, PizzaExtra
from exceptions import ObjectNotFoundError
from repositories.snacks_repo import PizzaExtraRepo, PizzaRepo
from schemas.shared import Pagination


class PizzaService:
    def __init__(self, pizza_repo: PizzaRepo, pizza_extra_repo: PizzaExtraRepo):
        self.pizza_repo = pizza_repo
        self.pizza_extra_repo = pizza_extra_repo

    async def get_pizzas(
        self,
        pagination: Pagination | None = None,
        filter_by: BaseModel | None = None,
    ) -> Tuple[List[Pizza], int]:
        pizzas, count = await self.pizza_repo.fetch_many_and_count(
            filter_by, pagination, prefetch=["available_extras", "ingredients"]
        )
        return pizzas, count

    async def get_pizza(self, _id: UUID) -> Pizza:
        try:
            pizza = await self.pizza_repo.fetch_one(
                {"id": _id}, prefetch=["available_extras", "ingredients"]
            )
        except DoesNotExist:
            raise ObjectNotFoundError(f"Pizza with {_id} does not exist.")
        return pizza

    async def get_pizza_extras(
        self, pizza_id: UUID, pagination: Pagination | None = None
    ) -> Tuple[List[PizzaExtra], int]:
        pizza_extras, count = await self.pizza_extra_repo.fetch_many_and_count(
            {"pizza_extra_available_fors__pizza_id": pizza_id}, pagination
        )
        return pizza_extras, count
