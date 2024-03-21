from repositories.snacks_repo import PizzaExtraRepo, PizzaRepo
from services.pizzas_service import PizzasService


def get_pizzas_service() -> PizzasService:
    return PizzasService(
        pizza_repo=PizzaRepo(),
        pizza_extra_repo=PizzaExtraRepo()
    )
