from pandas import DataFrame

from src.adapters.repositories.common.clickhouse_base import ClickHouseBaseRepository
from src.schemas.rsi import RSIQueryInputSchema


class RSIRepository(ClickHouseBaseRepository):
    # pylint: disable=duplicate-code
    async def query_rsi(self, input_schema: RSIQueryInputSchema) -> DataFrame:
        query = """
            SELECT
                exchange,
                section,
                ticker,
                interval,

                global_sma_high_rsi,
                global_sma_low_rsi,
                global_sma_sar_rsi,

                macro_trima_high_rsi,
                macro_trima_low_rsi,
                macro_trima_sar_rsi,

                macro_tema_high_rsi,
                macro_tema_low_rsi,
                macro_tema_sar_rsi,

                micro_trima_high_rsi,
                micro_trima_low_rsi,
                micro_trima_sar_rsi,

                micro_tema_high_rsi,
                micro_tema_low_rsi,
                micro_tema_sar_rsi,

                datetime
            FROM
                clickhouse.rsi
            WHERE
                exchange = %(exchange)s AND
                section = %(section)s AND
                ticker = %(ticker)s AND
                interval = %(interval)s
            ORDER BY
                datetime ASC
        """
        return await self._query_dataframe(query=query, parameters=input_schema.model_dump())

    # pylint: enable=duplicate-code

    async def truncate_rsi(self) -> None:
        table: str = "clickhouse.rsi"
        await self._truncate(table=table)

    async def insert_rsi(self, rsi: DataFrame) -> None:
        table: str = "clickhouse.rsi"
        await self._insert_dataframe(table=table, dataframe=rsi)
