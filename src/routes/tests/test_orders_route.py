import asyncio
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List
from uuid import UUID

import pytest
from httpx import AsyncClient

from db_models.orders import Order
from db_models.snacks import Pizza, PizzaExtra
from factories.orders_factory import build_order_in


@pytest.mark.asyncio
async def test_that_valid_order_can_be_created(client: AsyncClient) -> None:
    pizza_price = Decimal("45.00")
    extra_pricing = Decimal("1.50")

    pizza_quantity = 3
    extras_per_pizza_quantity = 3
    extra_quantity = 1  # each

    expected_total = (pizza_price * pizza_quantity) + (
        extra_pricing * extra_quantity * extras_per_pizza_quantity
    )

    pizza = await Pizza.all().first().prefetch_related("ingredients")
    pizza.price = pizza_price
    await pizza.save(update_fields=["price"])

    extras = await PizzaExtra.all().limit(extras_per_pizza_quantity)
    for extra in extras:
        extra.price = extra_pricing

    await asyncio.gather(*[extra.save(update_fields=["price"]) for extra in extras])

    order_in = build_order_in(
        pizza.id,
        [extra.id for extra in extras],
        extra_quantity=extra_quantity,
        pizza_quantity=pizza_quantity,
    )

    response = await client.post("/v1/orders", json=order_in)
    assert response.status_code == 201

    data = response.json()
    assert Decimal(data["total_cost"]) == expected_total
    assert data["name"] == order_in["name"]
    assert data["contact_phones"] == order_in["contact_phones"]
    assert data["delivery_address"] == order_in["delivery_address"]
    assert len(data["packages"]) == 1
    assert data["packages"][0]["pizza"]["id"] == str(pizza.id)
    assert data["packages"][0]["pizza"]["name"] == pizza.name
    assert Decimal(data["packages"][0]["pizza"]["price"]) == pizza.price

    sorted_ingredients = sorted(
        data["packages"][0]["pizza"]["ingredients"], key=lambda ing: ing["id"]
    )
    expected_ingredients = sorted(
        [{"id": str(ing.id), "name": ing.name} for ing in pizza.ingredients],
        key=lambda ing: ing["id"],
    )
    assert sorted_ingredients == expected_ingredients
    assert data["packages"][0]["pizza"]["images"] == pizza.images
    assert (
        datetime.fromisoformat(data["packages"][0]["pizza"]["created_at"])
        == pizza.created_at
    )
    assert (
        datetime.fromisoformat(data["packages"][0]["pizza"]["updated_at"])
        == pizza.updated_at
    )

    sorted_garnishes = sorted(
        data["packages"][0]["garnishes"], key=lambda g: g["extra"]["id"]
    )
    expected_garnishes = sorted(
        [
            {
                "extra": {
                    "id": str(extra.id),
                    "name": extra.name,
                    "price": str(extra.price),
                },
                "quantity": extra_quantity,
            }
            for extra in extras
        ],
        key=lambda e: e["extra"]["id"],
    )
    assert sorted_garnishes == expected_garnishes
    assert len(await Order.all()) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "override_field",
    [{"name": ""}, {"name": None}, {"contact_phones": []}, {"packages": []}],
)
async def test_that_valid_order_with_invalid_field_cannot_be_created(
    client: AsyncClient, override_field: Dict[str, Any]
) -> None:
    pizza = await Pizza.all().first().prefetch_related("ingredients")
    extras = await PizzaExtra.all().limit(3)

    order_in = build_order_in(pizza, extras)

    response = await client.post("/v1/orders", json={**order_in, **override_field})
    assert response.status_code == 422
