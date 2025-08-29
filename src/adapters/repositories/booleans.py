from pandas import DataFrame

from src.adapters.repositories.common.clickhouse_base import ClickHouseBaseRepository
from src.schemas.booleans import BooleansQueryInputSchema


class BooleansRepository(ClickHouseBaseRepository):
    # pylint: disable=duplicate-code
    async def query_booleans(self, input_schema: BooleansQueryInputSchema) -> DataFrame:
        # https://clickhouse.com/docs/ru/sql-reference/data-types/boolean
        query = """
            SELECT
                exchange,
                section,
                ticker,
                interval,

                is_global_sma_close_greater_than_global_sma_open,
                is_macro_trima_close_greater_than_macro_trima_open,
                is_macro_tema_close_greater_than_macro_tema_open,
                is_micro_trima_close_greater_than_micro_trima_open,
                is_micro_tema_close_greater_than_micro_tema_open,

                is_global_sma_low_greater_than_global_sma_sar,
                is_macro_trima_low_greater_than_macro_trima_sar,
                is_macro_tema_low_greater_than_macro_tema_sar,
                is_micro_trima_low_greater_than_micro_trima_sar,
                is_micro_tema_low_greater_than_micro_tema_sar,

                datetime
            FROM
                clickhouse.booleans
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

    async def truncate_booleans(self) -> None:
        table: str = "clickhouse.booleans"
        await self._truncate(table=table)

    async def insert_booleans(self, booleans: DataFrame) -> None:
        table: str = "clickhouse.booleans"
        await self._insert_dataframe(table=table, dataframe=booleans)
