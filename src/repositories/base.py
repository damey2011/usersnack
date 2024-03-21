from typing import Any, Dict, Generic, List, Tuple, Type, TypeVar

from pydantic import BaseModel
from tortoise import models

from schemas import Pagination

Model = TypeVar("Model", bound=models.Model)
Filter = BaseModel | Dict[str, Any]


class BaseRepository(Generic[Model]):
    model: Type[Model]

    @staticmethod
    def parse_filter(_filter: Filter) -> Dict[str, Any]:
        return _filter.model_dump(exclude_unset=True, exclude_none=True, by_alias=True) if isinstance(
            _filter,
            BaseModel
        ) else _filter

    async def fetch(self, *args, **kwargs) -> Model:
        return await self.model.get(*args, **kwargs)

    async def fetch_all(self, *args, **kwargs) -> List[Model]:
        return await self.model.all(*args, **kwargs)

    async def fetch_many(
        self,
        by: Filter,
        pagination: Pagination | None = None,
        prefetch: List[str] | None = None,
        select_related: List[str] | None = None,
        *args, **kwargs
    ) -> List[Model]:
        qs = self.model.filter(*args, **kwargs, **self.parse_filter(by))

        if pagination and pagination.offset:
            qs = qs.offset(pagination.offset)
        if pagination and pagination.limit:
            qs = qs.limit(pagination.limit)
        if prefetch:
            qs = qs.prefetch_related(*prefetch)
        if select_related:
            qs = qs.select_related(*select_related)

        return await qs

    async def count(self, by: Filter, **kwargs) -> int:
        return await self.model.filter(
            **kwargs,
            **self.parse_filter(by)
        ).count()

    async def fetch_many_and_count(
        self,
        by: Filter,
        pagination: Pagination | None = None,
        prefetch: List[str] | None = None,
        select_related: List[str] | None = None,
        *args, **kwargs
    ) -> Tuple[List[Model], int]:
        data = await self.fetch_many(by, pagination, prefetch, select_related, *args, **kwargs)
        count = await self.count(by, **kwargs)
        return data, count
