# pylint: disable=duplicate-code
from backtesting import Strategy
from numpy import ceil


# pylint: disable=attribute-defined-outside-init
class SARStrategy(Strategy):

    candle_prefix: str = "global_sma"
    allocation_percentage: int = 80

    # pylint: disable=protected-access
    def _compute_size(self) -> int:
        price: float = self.data.Open[-1]
        allocation: float = self._broker._cash * self._allocation_percentage
        return int(ceil(allocation / price))

    # pylint: enable=protected-access

    def _is_up_reversal(self) -> bool:
        return bool(self._data[self._boolean_column][-1] and self._data[self._streak_column][-1] == 1)  # noqa: WPS221

    def _is_down_reversal(self) -> bool:
        return bool(
            not self._data[self._boolean_column][-1] and self._data[self._streak_column][-1] == 1  # noqa: WPS221
        )

    def init(self) -> None:
        self._boolean_column: str = f"is_{self.candle_prefix}_low_greater_than_{self.candle_prefix}_sar"
        self._streak_column: str = f"{self._boolean_column}_streak"
        self._allocation_percentage: float = self.allocation_percentage / 10**2

    def next(self) -> None:
        if self._is_up_reversal():
            self.position.close()
            self.buy(size=self._compute_size())

        if self._is_down_reversal():
            self.position.close()


# pylint: enable=attribute-defined-outside-init,duplicate-code
