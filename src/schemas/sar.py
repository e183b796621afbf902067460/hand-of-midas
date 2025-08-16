from pydantic import BaseModel

from src.schemas.common.query_base import QueryInputBaseSchema


class SARInputSchema(BaseModel):
    prefix: str

    acceleration: float = 0.0075
    maximum: float = 0.015


class SARQueryInputSchema(QueryInputBaseSchema):
    """Input schema to get latest loaded SAR."""
