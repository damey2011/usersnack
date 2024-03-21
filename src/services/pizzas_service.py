from typing import List, Tuple
from uuid import UUID

from pydantic import BaseModel

from db_models.snacks import Pizza, PizzaExtra
from exceptions import ObjectNotFoundError
from repositories.snacks_repo import PizzaExtraRepo, PizzaRepo
from schemas import Pagination


class PizzasService:
    def __init__(
        self,
        pizza_repo: PizzaRepo,
        pizza_extra_repo: PizzaExtraRepo
    ):
        self.pizza_repo = pizza_repo
        self.pizza_extra_repo = pizza_extra_repo

    async def get_pizzas(
        self,
        pagination: Pagination | None = None,
        filter_by: BaseModel = None,
    ) -> Tuple[List[Pizza], int]:
        """
        :param pagination: offset and limit
        :param filter_by: A dictionary input of the filters to be applied to the queryset, already validated
        by the controller
        :return: A queryset of pizzas
        """
        pizzas, count = await self.pizza_repo.fetch_many_and_count(
            filter_by, pagination, prefetch=["available_extras", "ingredients"]
        )
        return pizzas, count

    async def get_pizza(self, _id: UUID) -> Pizza:
        # Using the `fetch_many` for single object as well to avoid implementing multiple prefetch methods
        matches = await self.pizza_repo.fetch_many(
            {"id": _id}, None, prefetch=["available_extras", "ingredients"]
        )
        if not len(matches):
            raise ObjectNotFoundError("Pizza requested cannot be found.")

        # We should not have more than more results, since we are fetching by unique ID, so no need to check
        # exact length
        return matches[0]

    async def get_pizza_extras(
        self,
        pizza_id: UUID,
        pagination: Pagination | None = None
    ) -> Tuple[List[PizzaExtra], int]:
        pizza_extras, count = await self.pizza_extra_repo.fetch_many_and_count(
            {"pizza_extra_available_fors__pizza_id": pizza_id},
            pagination
        )
        return pizza_extras, count
