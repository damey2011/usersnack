import pytest
from pydantic import ValidationError

from schemas.shared import Pagination


def test_that_pagination_offset_does_not_allow_negative_values():
    with pytest.raises(ValidationError):
        Pagination(offset=-1)


@pytest.mark.parametrize("param", [-1, 0])
def test_that_pagination_limit_does_not_allow_zero_or_negative_values(param: int):
    with pytest.raises(ValidationError):
        Pagination(limit=param)
