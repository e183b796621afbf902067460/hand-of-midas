from pandas import DataFrame

from src.adapters.repositories.common.clickhouse_base import ClickHouseBaseRepository
from src.schemas.streaks import StreaksQueryInputSchema


class StreaksRepository(ClickHouseBaseRepository):
    # pylint: disable=duplicate-code
    async def query_streaks(self, input_schema: StreaksQueryInputSchema) -> DataFrame:
        query = """
            SELECT
                exchange,
                section,
                ticker,
                interval,

                is_global_sma_close_greater_than_global_sma_open_streak,
                is_macro_trima_close_greater_than_macro_trima_open_streak,
                is_macro_tema_close_greater_than_macro_tema_open_streak,
                is_micro_trima_close_greater_than_micro_trima_open_streak,
                is_micro_tema_close_greater_than_micro_tema_open_streak,

                is_global_sma_low_greater_than_global_sma_sar_streak,
                is_macro_trima_low_greater_than_macro_trima_sar_streak,
                is_macro_tema_low_greater_than_macro_tema_sar_streak,
                is_micro_trima_low_greater_than_micro_trima_sar_streak,
                is_micro_tema_low_greater_than_micro_tema_sar_streak,

                datetime
            FROM
                clickhouse.streaks
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

    async def truncate_streaks(self) -> None:
        table: str = "clickhouse.streaks"
        await self._truncate(table=table)

    async def insert_streaks(self, streaks: DataFrame) -> None:
        table: str = "clickhouse.streaks"
        await self._insert_dataframe(table=table, dataframe=streaks)
