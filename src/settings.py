from datetime import datetime
from typing import Final

from pydantic import ClickHouseDsn, HttpUrl, IPvAnyAddress
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):

    APP_NAME: str = "hand-of-midas"
    APP_VERSION: str = "v0.0.1beta"
    APP_PORT: int = 8000
    APP_HOST: IPvAnyAddress = "0.0.0.0"  # type: ignore  # noqa: S104

    API_V1_ENDPOINT: str = "/api/v1"

    IS_DEBUG: bool = True
    IS_DEVELOPMENT: bool = True

    LOGLEVEL: str = "INFO"

    CLICKHOUSE_DSN: ClickHouseDsn = ClickHouseDsn("clickhouse+asynch://clickhouse:clickhouse@0.0.0.0:8123/clickhouse")

    BINANCE_SPOT_API_HTTP_URL: HttpUrl = HttpUrl("https://api.binance.com")
    BINANCE_SPOT_API_TIMEOUT: int = 60
    BINANCE_SPOT_API_RETRIES: int = 3

    BINANCE_USDTM_API_HTTP_URL: HttpUrl = HttpUrl("https://fapi.binance.com")
    BINANCE_USDTM_API_TIMEOUT: int = 60
    BINANCE_USDTM_API_RETRIES: int = 3

    TICKER: str = "BTCUSDT"

    TRIGGER_DATE: datetime = datetime.now()

    MILLISECONDS_IN_SECOND: Final[int] = 10**3
    DAYS_IN_YEAR: Final[int] = 365

    class Config:
        case_sensitive = True


settings: AppSettings = AppSettings()
