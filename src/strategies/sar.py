# pylint: disable=duplicate-code
from src.strategies.common.base import compute_size
from src.strategies.common.sar_base import SARStrategyBase


class SARStrategy(SARStrategyBase):

    rsi_threshold: int = 30
    rsi_column: str = "global_sma_sar_rsi"

    # pylint: disable=attribute-defined-outside-init
    def init(self) -> None:
        SARStrategyBase.init(self)
        self._is_upper_reversal: bool | None = None

    @property
    def _latest_rsi(self) -> float:
        return float(self.data[self.rsi_column][-1])

    def next(self) -> None:
        if self._is_up_reversal():
            self._is_upper_reversal = True

        if self._is_upper_reversal and self._latest_rsi < self.rsi_threshold and not self.position:
            self.position.close()
            self.buy(
                size=compute_size(
                    price=self._latest_close, cash=self._cash, allocation_percentage=self._allocation_percentage
                )
            )
            self._is_upper_reversal = False

        if self._is_down_reversal():
            self.position.close()
            self._is_upper_reversal = False

    # pylint: enable=attribute-defined-outside-init


# pylint: enable=duplicate-code
