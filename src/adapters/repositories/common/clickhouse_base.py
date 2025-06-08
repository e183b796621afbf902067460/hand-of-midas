from attr import attrs
from clickhouse_connect import get_async_client
from clickhouse_connect.driver.asyncclient import AsyncClient
from pandas import DataFrame

from src.settings import settings


async def get_clickhouse_client() -> AsyncClient:
    return await get_async_client(dsn=settings.CLICKHOUSE_DSN.unicode_string())


@attrs(slots=True, auto_attribs=True, kw_only=True)
class ClickHouseBaseRepository:
    _client: AsyncClient

    async def _query(self, query: str, parameters: tuple | None = None) -> DataFrame:
        return await self._client.query_df(query=query, parameters=parameters)
