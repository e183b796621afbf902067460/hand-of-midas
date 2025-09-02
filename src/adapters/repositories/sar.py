from pandas import DataFrame

from src.adapters.repositories.common.clickhouse_base import ClickHouseBaseRepository
from src.schemas.sar import SARQueryInputSchema


class SARRepository(ClickHouseBaseRepository):
    # pylint: disable=duplicate-code
    async def query_sar(self, input_schema: SARQueryInputSchema) -> DataFrame:
        query = """
            SELECT
                exchange,
                section,
                ticker,
                interval,

                global_sma_sar,
                macro_trima_sar,
                macro_tema_sar,
                micro_trima_sar,
                micro_tema_sar,

                datetime
            FROM
                clickhouse.sar
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

    async def truncate_sar(self) -> None:
        table: str = "clickhouse.sar"
        await self._truncate(table=table)

    async def insert_sar(self, sar: DataFrame) -> None:
        table: str = "clickhouse.sar"
        await self._insert_dataframe(table=table, dataframe=sar)
