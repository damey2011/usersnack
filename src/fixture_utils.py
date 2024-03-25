import json
from decimal import Decimal
from pathlib import Path
from typing import Dict, List

from tortoise import Tortoise

from db_models.snacks import Pizza, PizzaExtra, PizzaIngredient
from settings import settings

PARENT_DIR = Path(__file__).parent


async def load_db() -> None:
    await Tortoise.init(
        db_url=str(settings.get_postgres_dsn()),
        modules={"models": settings.TORTOISE_ORM_MODELS},
    )


async def save_pizzas(pizzas: List[Dict[str, str]]) -> None:
    ingredients: List[PizzaIngredient] = await PizzaIngredient.all()

    for pizza in pizzas:
        created_pizza = await Pizza.create(
            name=pizza["name"],
            price=Decimal(pizza["price"]),
            images=[f"{settings.MEDIA_PATH_PREFIX}/pizzas/{pizza['img']}"],
        )
        await created_pizza.ingredients.add(
            *list(filter(lambda ing: ing.name in pizza["ingredients"], ingredients))
        )
        print(f"Saved Pizza: {pizza['name']}")


async def save_ingredients(pizzas: List[Dict[str, str]]) -> None:
    all_ingredients = []

    for pizza in pizzas:
        all_ingredients += pizza["ingredients"]

    await PizzaIngredient.bulk_create(
        [PizzaIngredient(name=name) for name in set(all_ingredients)]
    )

    print("Saved Pizza Ingredients")


async def save_pizza_extras(pizza_extras: List[Dict[str, str]]) -> None:
    all_extras = []

    for extra in pizza_extras:
        all_extras.append(PizzaExtra(name=extra["name"], price=Decimal(extra["price"])))

    await PizzaExtra.bulk_create(all_extras)

    async for extra in PizzaExtra.all():
        # Allow all extras to be available to all Pizza for now.
        await extra.available_for.add(*(await Pizza.all()))

    print("Saved Pizza Extras")


async def load_fixtures() -> None:
    await load_db()
    fixtures_dir = Path(PARENT_DIR, "..", "fixtures")
    with open(Path(fixtures_dir, "pizzas.json")) as pizzas, open(
        Path(fixtures_dir, "pizza_extras.json")
    ) as pizza_extras:
        pizzas_list = json.load(pizzas)
        pizzas_extra_list = json.load(pizza_extras)

        await save_ingredients(pizzas_list)
        await save_pizzas(pizzas_list)
        await save_pizza_extras(pizzas_extra_list)
