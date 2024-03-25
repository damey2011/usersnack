from typing import Any, Dict, Generic, List, Tuple, Type, TypeVar

from pydantic import BaseModel
from tortoise import models

from schemas.shared import Pagination

Model = TypeVar("Model", bound=models.Model)
Filter = BaseModel | Dict[str, Any] | None


class BaseRepository(Generic[Model]):
    model: Type[Model]

    @staticmethod
    def _parse_filter(_filter: Filter) -> Dict[str, Any]:
        if not _filter:
            return {}

        return (
            _filter.model_dump(exclude_unset=True, exclude_none=True, by_alias=True)
            if isinstance(_filter, BaseModel)
            else _filter
        )

    async def save(self, **kwargs) -> Model:
        save_kwargs = {}
        for key in ["using_db", "update_fields", "force_create", "force_update"]:
            if key in kwargs:
                save_kwargs[key] = kwargs.pop(key)

        model = self.model(**kwargs)
        await model.save(**save_kwargs)
        return model

    async def fetch_one(
        self,
        by: Filter,
        prefetch: List[str] | None = None,
        select_related: List[str] | None = None,
    ) -> Model:
        qss = self.model.get(**self._parse_filter(by))

        if prefetch:
            qss = qss.prefetch_related(*prefetch)
        if select_related:
            qss = qss.select_related(*select_related)

        return await qss

    async def fetch_all(self, *args, **kwargs) -> List[Model]:
        return await self.model.all(*args, **kwargs)

    async def fetch_many(
        self,
        by: Filter,
        pagination: Pagination | None = None,
        prefetch: List[str] | None = None,
        select_related: List[str] | None = None,
    ) -> List[Model]:
        qs = self.model.filter(**self._parse_filter(by))

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
        return await self.model.filter(**kwargs, **self._parse_filter(by)).count()

    async def fetch_many_and_count(
        self,
        by: Filter = None,
        pagination: Pagination | None = None,
        prefetch: List[str] | None = None,
        select_related: List[str] | None = None,
    ) -> Tuple[List[Model], int]:
        data = await self.fetch_many(by, pagination, prefetch, select_related)
        count = await self.count(by)
        return data, count
