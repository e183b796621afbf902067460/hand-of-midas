# pylint: disable=duplicate-code
from asyncio import run

from clickhouse_connect.driver.asyncclient import AsyncClient as AsyncClickHouseClient
from pandas import DataFrame

from src.adapters.repositories.booleans import BooleansRepository
from src.adapters.repositories.common.clickhouse_base import get_clickhouse_client
from src.adapters.repositories.streaks import StreaksRepository
from src.schemas.booleans import BooleansQueryInputSchema
from src.schemas.common.binance_base import BinanceIntervalEnum, BinanceSectionEnum
from src.schemas.streaks import StreaksInputSchema
from src.services.booleans import BooleansService
from src.services.streaks import StreaksService
from src.settings import settings


async def main() -> None:
    section: BinanceSectionEnum = BinanceSectionEnum(value=settings.BINANCE_SECTION_NAME)  # type: ignore[call-overload]
    interval: BinanceIntervalEnum = BinanceIntervalEnum(value=settings.INTERVAL)  # type: ignore[call-overload]
    clickhouse_client: AsyncClickHouseClient = await get_clickhouse_client()
    booleans_service: BooleansService = BooleansService(repository=BooleansRepository(client=clickhouse_client))
    streaks_service: StreaksService = StreaksService(repository=StreaksRepository(client=clickhouse_client))
    # pylint: enable=duplicate-code

    booleans: DataFrame = await booleans_service.extract_booleans(
        input_schema=BooleansQueryInputSchema(
            ticker=settings.TICKER, exchange=settings.BINANCE_EXCHANGE_NAME, section=section, interval=interval
        )
    )

    streaks: DataFrame = StreaksService.compute_streak(
        booleans=booleans.copy(deep=True),
        input_schema=StreaksInputSchema(boolean_column="is_global_sma_close_greater_than_global_sma_open"),
    )

    streaks = StreaksService.compute_streak(
        booleans=streaks.copy(deep=True),
        input_schema=StreaksInputSchema(boolean_column="is_macro_trima_close_greater_than_macro_trima_open"),
    )
    streaks = StreaksService.compute_streak(
        booleans=streaks.copy(deep=True),
        input_schema=StreaksInputSchema(boolean_column="is_macro_tema_close_greater_than_macro_tema_open"),
    )

    streaks = StreaksService.compute_streak(
        booleans=streaks.copy(deep=True),
        input_schema=StreaksInputSchema(boolean_column="is_micro_trima_close_greater_than_micro_trima_open"),
    )
    streaks = StreaksService.compute_streak(
        booleans=streaks.copy(deep=True),
        input_schema=StreaksInputSchema(boolean_column="is_micro_tema_close_greater_than_micro_tema_open"),
    )

    streaks.drop(
        columns=[
            "is_global_sma_close_greater_than_global_sma_open",
            "is_macro_trima_close_greater_than_macro_trima_open",
            "is_macro_tema_close_greater_than_macro_tema_open",
            "is_micro_trima_close_greater_than_micro_trima_open",
            "is_micro_tema_close_greater_than_micro_tema_open",
        ],
        axis=1,
        inplace=True,
    )
    await streaks_service.truncate_streaks()
    await streaks_service.load_streaks(streaks=streaks)


if __name__ == "__main__":
    run(main=main())
