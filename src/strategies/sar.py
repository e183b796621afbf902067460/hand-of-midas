# pylint: disable=duplicate-code
from src.strategies.common.base import compute_size
from src.strategies.common.sar_base import SARStrategyBase


def _compute_allocation_percentage(
    allocation_percentage: float, latest_price: float, latest_global_sma: float
) -> float:
    return allocation_percentage if latest_price > latest_global_sma else allocation_percentage / 2


class SARStrategy(SARStrategyBase):

    rsi_threshold: int = 30
    rsi_column: str = "global_sma_sar_rsi"

    # pylint: disable=attribute-defined-outside-init
    def init(self) -> None:
        SARStrategyBase.init(self)
        self._is_bull_market: bool | None = None
        self._is_bear_market: bool | None = None

    @property
    def _latest_global_sma_close(self) -> float:
        return float(self.data["global_sma_close"][-1])

    @property
    def _latest_rsi(self) -> float:
        return float(self.data[self.rsi_column][-1])

    def next(self) -> None:
        if self._is_bull_reversal():
            self._is_bull_market = True
            self._is_bear_market = False
        if self._is_bear_reversal():
            self._is_bear_market = True
            self._is_bull_market = False

        if self._is_bull_market and self._latest_rsi < self.rsi_threshold and not self.position:
            self.position.close()
            self.buy(
                size=compute_size(
                    price=self._latest_close,
                    cash=self._cash,
                    allocation_percentage=_compute_allocation_percentage(
                        allocation_percentage=self._allocation_percentage,
                        latest_price=self._latest_close,
                        latest_global_sma=self._latest_global_sma_close,
                    ),
                )
            )

        if self._is_bear_market and self.position:
            self.position.close()

    # pylint: enable=attribute-defined-outside-init


# pylint: enable=duplicate-code
