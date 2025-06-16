from datetime import datetime
from typing import Final

from attr import attrs
from clickhouse_connect import get_async_client
from clickhouse_connect.driver.asyncclient import AsyncClient
from clickhouse_connect.driver.query import QueryResult
from pandas import DataFrame

from src.settings import settings

_CLICKHOUSE_UNIX_EPOCH_YEAR: Final[int] = 1970
_CLICKHOUSE_UNIX_EPOCH: Final[datetime] = datetime(year=_CLICKHOUSE_UNIX_EPOCH_YEAR, month=1, day=1, hour=0, minute=0)


def unix_epoch_to_none(timestamp: datetime) -> datetime | None:
    if timestamp == _CLICKHOUSE_UNIX_EPOCH:
        return None
    return timestamp


async def get_clickhouse_client() -> AsyncClient:
    return await get_async_client(dsn=settings.CLICKHOUSE_DSN.unicode_string())


@attrs(slots=True, auto_attribs=True, kw_only=True)
class ClickHouseBaseRepository:

    _client: AsyncClient

    async def _query(self, query: str, parameters: dict | None = None) -> QueryResult:
        return await self._client.query(query=query, parameters=parameters)

    async def _query_dataframe(self, query: str, parameters: dict | None = None) -> DataFrame:
        return await self._client.query_df(query=query, parameters=parameters)

    async def _insert_dataframe(self, table: str, dataframe: DataFrame) -> None:
        await self._client.insert_df(table=table, df=dataframe)
