from db_models.orders import Order
from repositories.orders_repo import OrderRepo


class OrdersService:
    def __init__(self, orders_repo: OrderRepo) -> None:
        self.orders_repo = orders_repo

    async def save_order(self) -> Order:
        pass
