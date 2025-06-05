from datetime import datetime

from pydantic import HttpUrl, IPvAnyAddress
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):

    APP_NAME: str = "the-hand-of-midas"
    APP_VERSION: str = "v0.0.1beta"
    APP_PORT: int = 8000
    APP_HOST: IPvAnyAddress = "0.0.0.0"  # type: ignore  # noqa: S104

    API_V1_ENDPOINT: str = "/api/v1"

    IS_DEBUG: bool = True
    IS_DEVELOPMENT: bool = True

    LOGLEVEL: str = "INFO"

    BINANCE_SPOT_API_HTTP_URL: HttpUrl = HttpUrl("https://api.binance.com")
    BINANCE_SPOT_API_TIMEOUT: int = 60
    BINANCE_SPOT_API_RETRIES: int = 3

    TRIGGER_DATE: datetime = datetime.now()

    MILLISECONDS_IN_SECOND: int = 10**3

    class Config:
        case_sensitive = True


settings: AppSettings = AppSettings()
