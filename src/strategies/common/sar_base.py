# pylint: disable=duplicate-code

from src.strategies.common.base import StrategyBase, compute_size


def _is_stop_and_reverse(streak: int) -> bool:
    return bool(streak == 1)


class SARStrategyBase(StrategyBase):

    sar_prefix: str = "global_sma"

    # pylint: disable=attribute-defined-outside-init
    def init(self) -> None:
        StrategyBase.init(self)
        self._boolean_column: str = f"is_{self.sar_prefix}_low_greater_than_{self.sar_prefix}_sar"
        self._streak_column: str = f"{self._boolean_column}_streak"

    # pylint: enable=attribute-defined-outside-init

    @property
    def _latest_boolean(self) -> bool:
        return bool(self._data[self._boolean_column][-1])

    @property
    def _latest_streak(self) -> int:
        return int(self._data[self._streak_column][-1])

    def _is_bull_reversal(self) -> bool:
        return bool(self._latest_boolean and _is_stop_and_reverse(streak=self._latest_streak))  # noqa: WPS221

    def _is_bear_reversal(self) -> bool:
        return bool(not self._latest_boolean and _is_stop_and_reverse(streak=self._latest_streak))  # noqa: WPS221

    def next(self) -> None:
        if self._is_bull_reversal():
            self.position.close()
            self.buy(
                size=compute_size(
                    price=self._latest_close, cash=self._cash, allocation_percentage=self._allocation_percentage
                )
            )

        if self._is_bear_reversal():
            self.position.close()


# pylint: enable=duplicate-code
