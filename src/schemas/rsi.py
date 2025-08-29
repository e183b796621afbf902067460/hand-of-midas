from pydantic import BaseModel

from src.schemas.common.query_base import QueryInputBaseSchema


class RSIInputSchema(BaseModel):
    column: str

    period: int


class RSIQueryInputSchema(QueryInputBaseSchema):
    """Input schema to get latest loaded RSI."""
