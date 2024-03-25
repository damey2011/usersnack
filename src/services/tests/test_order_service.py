import uuid
from unittest.mock import AsyncMock

import pytest

from factories.orders_factory import build_order_in
from schemas.orders import OrderIn
from services.order_service import OrderService


@pytest.mark.asyncio
async def test_that_order_service_saves_the_order() -> None:
    mock_repo = AsyncMock()
    orders_service = OrderService(order_repo=mock_repo)
    await orders_service.save_order(
        OrderIn(
            **build_order_in(
                pizza_id=uuid.uuid4(), extras=[uuid.uuid4() for _ in range(5)]
            )
        )
    )
    assert mock_repo.save.call_count == 1
