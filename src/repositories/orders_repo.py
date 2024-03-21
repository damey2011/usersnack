from db_models.orders import Order
from repositories.base import BaseRepository


class OrderRepo(BaseRepository[Order]):
    model = Order
