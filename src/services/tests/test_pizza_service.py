import uuid
from unittest.mock import AsyncMock

import pytest
from tortoise.exceptions import DoesNotExist

from exceptions import ObjectNotFoundError
from factories.orders_factory import build_order_in
from schemas.orders import OrderIn
from services.order_service import OrderService
from services.pizza_service import PizzaService


@pytest.mark.asyncio
async def test_that_pizza_service_get_pizzas_retrieves_from_repo() -> None:
    mock_pizza_repo = AsyncMock()
    mock_pizza_extra_repo = AsyncMock()
    pizza_service = PizzaService(
        pizza_repo=mock_pizza_repo, pizza_extra_repo=mock_pizza_extra_repo
    )
    mock_pizza_repo.fetch_many_and_count.return_value = ([], 0)
    await pizza_service.get_pizzas()
    assert mock_pizza_repo.fetch_many_and_count.call_count == 1


@pytest.mark.asyncio
async def test_that_pizza_service_get_pizza_raises_object_not_found_when_it_does_not_exist() -> None:
    mock_pizza_repo = AsyncMock()
    mock_pizza_extra_repo = AsyncMock()
    pizza_service = PizzaService(
        pizza_repo=mock_pizza_repo, pizza_extra_repo=mock_pizza_extra_repo
    )
    mock_pizza_repo.fetch_one.side_effect = DoesNotExist("Pizza does not exist")
    with pytest.raises(ObjectNotFoundError):
        await pizza_service.get_pizza(uuid.uuid4())
    assert mock_pizza_repo.fetch_one.call_count == 1
