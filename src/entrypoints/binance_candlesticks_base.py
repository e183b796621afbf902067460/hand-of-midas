from asyncio import run
from datetime import datetime

from clickhouse_connect.driver.asyncclient import AsyncClient as AsyncClickHouseClient
from httpx import AsyncClient as HTTPAsyncClient
from httpx import AsyncHTTPTransport
from pandas import DataFrame

from src.adapters.clients.binance import BinanceSpotAPIClient, BinanceUsdtmAPIClient
from src.adapters.repositories.candlesticks import CandlesticksRepository
from src.adapters.repositories.common.clickhouse_base import get_clickhouse_client
from src.schemas.binance import BinanceKlinesInputSchema
from src.schemas.candlesticks import CandlesticksLatestTimestampQueryInputSchema
from src.schemas.common.binance_base import BinanceIntervalEnum, BinanceSectionEnum
from src.services.binance import BinanceService
from src.services.candlesticks import CandlesticksService
from src.settings import settings


# pylint: disable=too-many-locals
async def main() -> None:
    section: BinanceSectionEnum = BinanceSectionEnum(value=settings.BINANCE_SECTION_NAME)  # type: ignore[call-overload]
    interval: BinanceIntervalEnum = BinanceIntervalEnum(value=settings.INTERVAL)  # type: ignore[call-overload]
    binance_api_session: HTTPAsyncClient = HTTPAsyncClient(
        base_url=settings.BINANCE_SPOT_API_HTTP_URL.unicode_string()
        if section is BinanceSectionEnum.BINANCE_SPOT
        else settings.BINANCE_USDTM_API_HTTP_URL.unicode_string(),
        timeout=settings.BINANCE_SPOT_API_TIMEOUT
        if section is BinanceSectionEnum.BINANCE_SPOT
        else settings.BINANCE_USDTM_API_TIMEOUT,
        transport=AsyncHTTPTransport(
            retries=settings.BINANCE_SPOT_API_RETRIES
            if section is BinanceSectionEnum.BINANCE_SPOT
            else settings.BINANCE_USDTM_API_RETRIES,
            http2=True,
        ),
    )
    binance_api_client: BinanceSpotAPIClient | BinanceUsdtmAPIClient = (
        BinanceSpotAPIClient(session=binance_api_session)
        if section is BinanceSectionEnum.BINANCE_SPOT
        else BinanceUsdtmAPIClient(session=binance_api_session)
    )
    await binance_api_client.ping()
    clickhouse_client: AsyncClickHouseClient = await get_clickhouse_client()
    candlesticks_repository: CandlesticksRepository = CandlesticksRepository(client=clickhouse_client)
    candlesticks_service: CandlesticksService = CandlesticksService(repository=candlesticks_repository)
    binance_service: BinanceService = BinanceService(client=binance_api_client)

    latest_timestamp: datetime = await candlesticks_service.extract_latest_timestamp(
        input_schema=CandlesticksLatestTimestampQueryInputSchema(
            ticker=settings.TICKER, exchange=settings.BINANCE_EXCHANGE_NAME, section=section, interval=interval
        )
    )
    candlesticks: DataFrame = await binance_service.get_klines(
        input_schema=BinanceKlinesInputSchema(
            symbol=settings.TICKER,
            section=section,
            interval=interval,
            start_time=latest_timestamp,
            end_time=settings.TRIGGER_DATE,
        )
    )
    candlesticks.drop_duplicates(inplace=True)
    await candlesticks_service.load_candlesticks(candlesticks=candlesticks)


# pylint: enable=too-many-locals


if __name__ == "__main__":
    run(main=main())
