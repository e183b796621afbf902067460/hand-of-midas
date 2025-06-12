from datetime import datetime

from clickhouse_connect.driver.query import QueryResult
from pandas import DataFrame

from src.adapters.repositories.common.clickhouse_base import ClickHouseBaseRepository
from src.schemas.candlesticks import CandlesticksInputSchema, CandlesticksLatestTimestampInputSchema


class CandlesticksRepository(ClickHouseBaseRepository):
    async def query_latest_timestamp(self, input_schema: CandlesticksLatestTimestampInputSchema) -> datetime | None:
        query: str = """
            SELECT
                MAX(close_time) AS latest_timestamp
            FROM
                clickhouse.candlesticks
            WHERE
                ticker = %(ticker)s AND
                exchange = %(exchange)s AND
                interval = %(interval)s
        """
        query_result: QueryResult = await self._query(query=query, parameters=input_schema.model_dump())
        return ClickHouseBaseRepository._unix_epoch_to_none(timestamp=query_result.first_item["latest_timestamp"])

    async def query_candlesticks(self, input_schema: CandlesticksInputSchema) -> DataFrame:
        query = """
            SELECT
                open,
                high,
                low,
                close,
                open_time,
                close_time
            FROM
                clickhouse.candlesticks
            WHERE
                ticker = %(ticker)s AND
                exchange = %(exchange)s AND
                interval = %(interval)s
        """
        return await self._query_dataframe(query=query, parameters=input_schema.model_dump())

    async def insert_candlesticks(self, dataframe: DataFrame) -> None:
        table: str = "clickhouse.candlesticks"
        await self._insert_dataframe(table=table, dataframe=dataframe)
