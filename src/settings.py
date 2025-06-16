from datetime import datetime
from typing import Final

from pydantic import ClickHouseDsn, HttpUrl, IPvAnyAddress
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):

    APP_NAME: str = "hand-of-midas"
    APP_VERSION: str = "v0.0.1-alpha"
    APP_PORT: int = 8000
    APP_HOST: IPvAnyAddress = "0.0.0.0"  # type: ignore  # noqa: S104

    API_V1_ENDPOINT: str = "/api/v1"

    IS_DEBUG: bool = True
    IS_DEVELOPMENT: bool = True

    LOGLEVEL: str = "INFO"

    CLICKHOUSE_DSN: ClickHouseDsn

    BINANCE_EXCHANGE_NAME: Final[str] = "Binance"
    BINANCE_SECTION_NAME: str = "SPOT"

    BINANCE_SPOT_API_HTTP_URL: HttpUrl = HttpUrl("https://api.binance.com")
    BINANCE_SPOT_API_TIMEOUT: int = 60
    BINANCE_SPOT_API_RETRIES: int = 3

    BINANCE_USDTM_API_HTTP_URL: HttpUrl = HttpUrl("https://fapi.binance.com")
    BINANCE_USDTM_API_TIMEOUT: int = 60
    BINANCE_USDTM_API_RETRIES: int = 3

    TICKER: str
    INTERVAL: str

    TRIGGER_DATE: datetime = datetime.now()
    YEARS_AGO: int = 10

    MILLISECONDS_IN_SECOND: Final[int] = 10**3
    DAYS_IN_YEAR: Final[int] = 365

    class Config:
        case_sensitive = True


settings: AppSettings = AppSettings()
