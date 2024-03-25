from db_models.orders import Order
from repositories.orders_repo import OrderRepo
from schemas.orders import OrderIn


class OrderService:
    def __init__(self, order_repo: OrderRepo) -> None:
        self.order_repo = order_repo

    async def save_order(self, order_in: OrderIn) -> Order:
        order = await self.order_repo.save(order_in)
        # Things we can do here:
        # - Send them an order confirmation via SMS
        # - Run some non-format validation on information provided. e.g. Address validation, phone number validation
        return order
