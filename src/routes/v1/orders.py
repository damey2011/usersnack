from fastapi import APIRouter, Depends
from starlette import status

from deps import get_order_service
from schemas.orders import OrderIn, OrderOut
from services.order_service import OrderService

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=OrderOut)
async def create_order(
    order_in: OrderIn, order_service: OrderService = Depends(get_order_service)
) -> OrderOut:
    order = await order_service.save_order(order_in)
    return OrderOut.from_orm(order)
