from pydantic import BaseModel

from src.schemas.common.query_base import QueryInputBaseSchema


class BooleansInputSchema(BaseModel):
    first_column: str
    second_column: str


class BooleansQueryInputSchema(QueryInputBaseSchema):
    """Input schema to get latest loaded boolean features."""
