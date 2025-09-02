from pydantic import BaseModel

from src.schemas.common.query_base import QueryInputBaseSchema


class StreaksInputSchema(BaseModel):
    boolean_column: str


class StreaksQueryInputSchema(QueryInputBaseSchema):
    """Input schema to get latest loaded streaks."""
