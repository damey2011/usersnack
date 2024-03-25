from decimal import Decimal

import pytest
from httpx import AsyncClient

from db_models.snacks import Pizza


@pytest.mark.asyncio
async def test_pizzas_list_returns_valid_list(client: AsyncClient) -> None:
    response = await client.get("/v1/pizzas")
    assert response.status_code == 200

    data = response.json()
    assert data["offset"] == 0
    assert data["limit"] == 10
    assert len(data["results"]) == 10
    assert data["results"][0]["name"] is not None
    assert data["results"][0]["price"] is not None
    assert data["results"][0]["ingredients"] is not None
    assert isinstance(data["results"][0]["ingredients"], list)
    assert isinstance(data["results"][0]["images"], list)
    assert len(data["results"][0]["ingredients"])
    assert len(data["results"][0]["images"])


@pytest.mark.asyncio
async def test_pizzas_list_pagination_works(client: AsyncClient) -> None:
    response = await client.get("/v1/pizzas", params={"offset": 0, "limit": 10})
    assert response.status_code == 200
    data1 = response.json()

    response = await client.get("/v1/pizzas", params={"offset": 10, "limit": 10})
    assert response.status_code == 200
    data2 = response.json()

    assert data1 != data2
    assert data1["offset"] == 0
    assert data2["offset"] == 10


@pytest.mark.asyncio
async def test_can_search_pizza_by_name(client: AsyncClient) -> None:
    response = await client.get("/v1/pizzas", params={"name": "Chicken"})
    assert response.status_code == 200
    data = response.json()

    for result in data["results"]:
        assert "Chicken" in result["name"]


@pytest.mark.asyncio
async def test_can_retrieve_single_pizza(client: AsyncClient) -> None:
    pizza = await Pizza.all().first()

    response = await client.get(f"/v1/pizzas/{pizza.id}")
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == str(pizza.id)
    assert data["name"] == pizza.name
    assert Decimal(data["price"]) == pizza.price
    assert data["images"] == pizza.images
