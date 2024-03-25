from repositories.orders_repo import OrderRepo
from repositories.snacks_repo import PizzaExtraRepo, PizzaRepo
from services.order_service import OrderService
from services.pizza_service import PizzaService


def get_pizza_service() -> PizzaService:
    return PizzaService(pizza_repo=PizzaRepo(), pizza_extra_repo=PizzaExtraRepo())


def get_order_service() -> OrderService:
    return OrderService(
        order_repo=OrderRepo(),
    )
