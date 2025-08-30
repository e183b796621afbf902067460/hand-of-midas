# pylint: disable=duplicate-code

from src.strategies.common.base import StrategyBase, compute_size


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

    def _is_up_reversal(self) -> bool:
        return bool(self._latest_boolean and self._latest_streak == 1)  # noqa: WPS221

    def _is_down_reversal(self) -> bool:
        return bool(not self._latest_boolean and self._latest_streak == 1)  # noqa: WPS221

    def next(self) -> None:
        if self._is_up_reversal():
            self.position.close()
            self.buy(
                size=compute_size(
                    price=self._latest_close, cash=self._cash, allocation_percentage=self._allocation_percentage
                )
            )

        if self._is_down_reversal():
            self.position.close()


# pylint: enable=duplicate-code
