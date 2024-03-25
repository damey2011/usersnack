from fastapi import APIRouter

from routes.v1.orders import router as order_router
from routes.v1.pizzas import router as pizza_router

v1_router = APIRouter()

v1_router.include_router(pizza_router, prefix="/pizzas")
v1_router.include_router(order_router, prefix="/orders")
