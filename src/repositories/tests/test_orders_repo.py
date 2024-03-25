import uuid
from decimal import Decimal
from unittest.mock import AsyncMock

from pytest_mock import MockerFixture

from db_models.orders import Order
from factories.orders_factory import build_order_in
from repositories.orders_repo import (BaseRepository, OrderPackage,
                                      OrderPackageGarnish, OrderRepo)
from schemas.orders import OrderIn


async def test_that_all_order_entities_are_persisted(mocker: MockerFixture) -> None:
    # Prepare the Order Object
    order_in = build_order_in(uuid.uuid4(), [uuid.uuid4()])
    order_obj = AsyncMock(
        wraps=Order(
            id=uuid.uuid4(),
            name="Damilola",
            contact_phones=["08123949438"],
            delivery_address=order_in["delivery_address"],
            total_cost=Decimal("50.00"),
        )
    )

    # Prepare the Connections that are used to make the raw queries in the `compute_cost` method
    mock_connection_obj = AsyncMock()
    mock_connection_obj.execute_query.side_effect = [
        [1, [{"total_extra_cost": Decimal("0.00")}]],
        [1, [{"total_pizza_cost": Decimal("50.00")}]],
    ]
    mock_connections = mocker.patch("repositories.orders_repo.connections")
    mock_connections.get.return_value = mock_connection_obj

    # Mock the transaction contextmanager and functions/methods that could reach the database
    mock_base_repo_save = AsyncMock(return_value=order_obj)
    mock_in_transaction = mocker.patch("repositories.orders_repo.in_transaction")
    mocker.patch.multiple(
        BaseRepository, fetch_one=AsyncMock(), save=mock_base_repo_save
    )
    mock_order_package_bulk_save = mocker.patch.object(
        OrderPackage, "bulk_create", new_callable=AsyncMock
    )
    mock_order_package_garnish_bulk_save = mocker.patch.object(
        OrderPackageGarnish, "bulk_create", new_callable=AsyncMock
    )
    order_obj.save.return_value = order_obj
    orders_repo = OrderRepo()

    # Execute the save method as Act
    await orders_repo.save(OrderIn(**order_in))

    # Make assertions
    assert mock_in_transaction.call_count == 1
    assert mock_order_package_bulk_save.call_count == 1
    assert mock_order_package_garnish_bulk_save.call_count == 1
    assert order_obj.save.call_count == 1
    assert mock_base_repo_save.call_count == 1
    assert mock_connection_obj.execute_query.call_count == 2
