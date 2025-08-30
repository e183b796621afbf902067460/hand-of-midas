from backtesting import Strategy
from numpy import ceil


class StrategyBase(Strategy):
    allocation_percentage: int = 80

    # pylint: disable=attribute-defined-outside-init
    def init(self) -> None:
        self._allocation_percentage: float = self.allocation_percentage / 10**2

    # pylint: enable=attribute-defined-outside-init

    # pylint: disable=protected-access
    @property
    def _cash(self) -> float:
        return float(self._broker._cash)

    # pylint: enable=protected-access

    @property
    def _latest_open(self) -> float:
        return float(self.data.Open[-1])

    @property
    def _latest_high(self) -> float:
        return float(self.data.High[-1])

    @property
    def _latest_low(self) -> float:
        return float(self.data.Low[-1])

    @property
    def _latest_close(self) -> float:
        return float(self.data.Close[-1])

    def next(self) -> None:
        ...


def compute_size(price: float, cash: float, allocation_percentage: float) -> int:
    allocation: float = cash * allocation_percentage
    return int(ceil(allocation / price))
