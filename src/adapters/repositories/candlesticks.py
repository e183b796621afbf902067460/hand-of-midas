from datetime import datetime

from clickhouse_connect.driver.query import QueryResult
from pandas import DataFrame

from src.adapters.repositories.common.clickhouse_base import ClickHouseBaseRepository, unix_epoch_to_none
from src.schemas.candlesticks import CandlesticksInputSchema, CandlesticksLatestTimestampInputSchema


class CandlesticksRepository(ClickHouseBaseRepository):
    # pylint: disable=duplicate-code
    async def query_latest_timestamp(self, input_schema: CandlesticksLatestTimestampInputSchema) -> datetime | None:
        query: str = """
            SELECT
                MAX(close_time) AS latest_timestamp
            FROM
                clickhouse.candlesticks
            WHERE
                ticker = %(ticker)s AND
                exchange = %(exchange)s AND
                section = %(section)s AND
                interval = %(interval)s
        """
        query_result: QueryResult = await self._query(query=query, parameters=input_schema.model_dump())
        return unix_epoch_to_none(timestamp=query_result.first_item["latest_timestamp"])

    # pylint: enable=duplicate-code

    # pylint: disable=duplicate-code
    async def query_candlesticks(self, input_schema: CandlesticksInputSchema) -> DataFrame:
        query = """
            SELECT
                open,
                high,
                low,
                close,
                close_time + INTERVAL 1 SECOND AS datetime
            FROM
                clickhouse.candlesticks
            WHERE
                ticker = %(ticker)s AND
                exchange = %(exchange)s AND
                section = %(section)s AND
                interval = %(interval)s
            ORDER BY
                datetime ASC
        """
        return await self._query_dataframe(query=query, parameters=input_schema.model_dump())

    # pylint: enable=duplicate-code

    async def insert_candlesticks(self, candlesticks: DataFrame) -> None:
        table: str = "clickhouse.candlesticks"
        await self._insert_dataframe(table=table, dataframe=candlesticks)
