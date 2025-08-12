from datetime import timedelta
from enum import Enum


class _BinanceBaseException(Exception):
    """Base Binance exception."""


class _NoSuchIntervalException(_BinanceBaseException):
    """Exception to raise when wrong interval provided."""


class BinanceSectionEnum(str, Enum):

    BINANCE_SPOT = "SPOT"
    BINANCE_USDTM = "USDT-M"


class BinanceIntervalEnum(str, Enum):

    ONE_SECOND = "1s"

    ONE_MINUTE = "1m"
    THREE_MINUTES = "3m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    THIRTY_MINUTES = "30m"

    ONE_HOUR = "1h"
    TWO_HOURS = "2h"
    FOUR_HOURS = "4h"
    SIX_HOURS = "6h"
    EIGHT_HOURS = "8h"
    TWELVE_HOURS = "12h"

    ONE_DAY = "1d"
    THREE_DAYS = "3d"

    ONE_WEEK = "1w"

    # pylint: disable=too-complex, too-many-branches, too-many-statements
    @staticmethod
    def total_seconds(interval: "BinanceIntervalEnum") -> float:  # noqa: WPS231
        total_seconds: float | None = None
        if interval is BinanceIntervalEnum.ONE_SECOND.value:  # noqa: WPS223
            total_seconds = timedelta(seconds=1).total_seconds()
        elif interval is BinanceIntervalEnum.ONE_MINUTE.value:
            total_seconds = timedelta(minutes=1).total_seconds()
        elif interval is BinanceIntervalEnum.THREE_MINUTES.value:
            total_seconds = timedelta(minutes=3).total_seconds()
        elif interval is BinanceIntervalEnum.FIVE_MINUTES.value:
            total_seconds = timedelta(minutes=5).total_seconds()
        elif interval is BinanceIntervalEnum.FIFTEEN_MINUTES.value:
            total_seconds = timedelta(minutes=15).total_seconds()  # noqa: WPS432
        elif interval is BinanceIntervalEnum.THIRTY_MINUTES.value:
            total_seconds = timedelta(minutes=30).total_seconds()  # noqa: WPS432
        elif interval is BinanceIntervalEnum.ONE_HOUR.value:
            total_seconds = timedelta(hours=1).total_seconds()
        elif interval is BinanceIntervalEnum.TWO_HOURS.value:
            total_seconds = timedelta(hours=2).total_seconds()
        elif interval is BinanceIntervalEnum.FOUR_HOURS.value:
            total_seconds = timedelta(hours=4).total_seconds()
        elif interval is BinanceIntervalEnum.SIX_HOURS.value:
            total_seconds = timedelta(hours=6).total_seconds()
        elif interval is BinanceIntervalEnum.EIGHT_HOURS.value:
            total_seconds = timedelta(hours=8).total_seconds()
        elif interval is BinanceIntervalEnum.TWELVE_HOURS.value:
            total_seconds = timedelta(hours=12).total_seconds()  # noqa: WPS432
        elif interval is BinanceIntervalEnum.ONE_DAY.value:
            total_seconds = timedelta(days=1).total_seconds()
        elif interval is BinanceIntervalEnum.THREE_DAYS.value:
            total_seconds = timedelta(days=3).total_seconds()
        elif interval is BinanceIntervalEnum.ONE_WEEK.value:
            total_seconds = timedelta(weeks=1).total_seconds()

        if not total_seconds:
            raise _NoSuchIntervalException(f"There is no such interval `{interval}`.")

        return total_seconds


# pylint: enable=too-complex, too-many-branches, too-many-statements
