from pandas import DataFrame

from src.adapters.repositories.common.clickhouse_base import ClickHouseBaseRepository
from src.schemas.smoothing import SmoothedCandlesticksInputSchema


class SmoothedCandlesticksRepository(ClickHouseBaseRepository):
    # pylint: disable=duplicate-code
    async def query_smoothed_candlesticks(self, input_schema: SmoothedCandlesticksInputSchema) -> DataFrame:
        query = """
            SELECT
                global_sma_open,
                global_sma_high,
                global_sma_low,
                global_sma_close,

                macro_trima_open,
                macro_trima_high,
                macro_trima_low,
                macro_trima_close,

                macro_tema_open,
                macro_tema_high,
                macro_tema_low,
                macro_tema_close,

                micro_trima_open,
                micro_trima_high,
                micro_trima_low,
                micro_trima_close,

                micro_tema_open,
                micro_tema_high,
                micro_tema_low,
                micro_tema_close,

                datetime
            FROM
                clickhouse.smoothed_candlesticks
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

    async def truncate_smoothed_candlesticks(self) -> None:
        table: str = "clickhouse.smoothed_candlesticks"
        await self._truncate(table=table)

    async def insert_smoothed_candlesticks(self, smoothed_candlesticks: DataFrame) -> None:
        table: str = "clickhouse.smoothed_candlesticks"
        await self._insert_dataframe(table=table, dataframe=smoothed_candlesticks)
