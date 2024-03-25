from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status

from deps import get_pizza_service
from error_codes import UserSnackErrorCode
from schemas.shared import PaginatedUserSnackResponse, Pagination
from schemas.snacks import PizzaExtraOut, PizzaFilter, PizzaOut
from services.pizza_service import PizzaService

router = APIRouter()


@router.get(
    "",
    response_model=PaginatedUserSnackResponse[PizzaOut],
    status_code=status.HTTP_200_OK,
    summary="Fetch and search through Pizzas",
)
async def get_pizzas(
    pizza_service: PizzaService = Depends(get_pizza_service),
    pagination: Pagination = Depends(),
    pizza_filter: PizzaFilter = Depends(),
) -> PaginatedUserSnackResponse[PizzaOut]:
    """
    **Query Filters:**
    - `name`: Finds Pizzas with keyword specified in name.
    """
    pizzas, count = await pizza_service.get_pizzas(pagination, pizza_filter)
    results = [PizzaOut.from_orm(pizza) for pizza in pizzas]
    return PaginatedUserSnackResponse(
        results=results, size=count, **pagination.model_dump()
    )


@router.get(
    "/{_id}",
    response_model=PizzaOut,
    status_code=status.HTTP_200_OK,
    summary="Get single Pizza by ID",
    responses={404: {"code": UserSnackErrorCode.NOT_FOUND}},
)
async def get_pizza(
    _id: UUID,
    pizza_service: PizzaService = Depends(get_pizza_service),
) -> PizzaOut:
    pizza = await pizza_service.get_pizza(_id)
    return PizzaOut.from_orm(pizza)


@router.get(
    "/{_id}/extras",
    response_model=PaginatedUserSnackResponse[PizzaExtraOut],
    status_code=status.HTTP_200_OK,
    summary="Fetch Pizza Extras",
)
async def get_pizza_extras(
    _id: UUID,
    pizza_service: PizzaService = Depends(get_pizza_service),
    pagination: Pagination = Depends(),
) -> PaginatedUserSnackResponse[PizzaExtraOut]:
    pizza_extras, count = await pizza_service.get_pizza_extras(_id, pagination)

    results = []
    for extra in pizza_extras:
        results.append(PizzaExtraOut(id=extra.id, name=extra.name, price=extra.price))

    return PaginatedUserSnackResponse(
        results=results, size=count, **pagination.model_dump()
    )
