# pylint: disable=duplicate-code

from src.strategies.common.base import StrategyBase, compute_size


def _is_stop_and_reverse(streak: int) -> bool:
    return bool(streak == 1)


class BullishSARStrategy(StrategyBase):

    sar_on_long: str = "global_sma"

    # pylint: disable=attribute-defined-outside-init
    def init(self) -> None:
        StrategyBase.init(self)
        self._boolean_on_long: str = f"is_{self.sar_on_long}_low_greater_than_{self.sar_on_long}_sar"
        self._streak_on_long: str = f"{self._boolean_on_long}_streak"

    # pylint: enable=attribute-defined-outside-init

    @property
    def _latest_boolean_on_long(self) -> bool:
        return bool(self._data[self._boolean_on_long][-1])

    @property
    def _latest_streak_on_long(self) -> int:
        return int(self._data[self._streak_on_long][-1])

    def _is_bullish_market(self) -> bool:
        return bool(self.data.Close[-1] > self._latest_global_sma)

    def _is_bullish_reversal_on_long(self) -> bool:
        return bool(
            self._latest_boolean_on_long and _is_stop_and_reverse(streak=self._latest_streak_on_long)
        )  # noqa: WPS221

    def _is_bearish_reversal_on_long(self) -> bool:
        return bool(
            not self._latest_boolean_on_long and _is_stop_and_reverse(streak=self._latest_streak_on_long)
        )  # noqa: WPS221

    # pylint: disable=attribute-defined-outside-init
    def next(self) -> None:
        if self._is_bullish_reversal_on_long() and self._is_bullish_market() and not self.position.is_long:
            self.position.close()
            self.buy(
                size=compute_size(
                    price=self.data.Close[-1],
                    cash=self._cash,
                    allocation_percentage=self._allocation_percentage,
                ),
                tag=self._cash,
            )

        if self._is_bearish_reversal_on_long() and self.position.is_long:
            self.position.close()

        # pylint: enable=attribute-defined-outside-init


class BearishSARStrategy(StrategyBase):

    sar_on_short: str = "global_sma"

    # pylint: disable=attribute-defined-outside-init
    def init(self) -> None:
        StrategyBase.init(self)
        self._boolean_on_short: str = f"is_{self.sar_on_short}_low_greater_than_{self.sar_on_short}_sar"
        self._streak_on_short: str = f"{self._boolean_on_short}_streak"

    # pylint: enable=attribute-defined-outside-init

    @property
    def _latest_boolean_on_short(self) -> bool:
        return bool(self._data[self._boolean_on_short][-1])

    @property
    def _latest_streak_on_short(self) -> int:
        return int(self._data[self._streak_on_short][-1])

    def _is_bearish_market(self) -> bool:
        return bool(self.data.Close[-1] < self._latest_global_sma)

    def _is_bullish_reversal_on_short(self) -> bool:
        return bool(
            self._latest_boolean_on_short and _is_stop_and_reverse(streak=self._latest_streak_on_short)
        )  # noqa: WPS221

    def _is_bearish_reversal_on_short(self) -> bool:
        return bool(
            not self._latest_boolean_on_short and _is_stop_and_reverse(streak=self._latest_streak_on_short)
        )  # noqa: WPS221

    # pylint: disable=attribute-defined-outside-init
    def next(self) -> None:
        if self._is_bearish_reversal_on_short() and self._is_bearish_market() and not self.position.is_short:
            self.position.close()
            self.sell(
                size=compute_size(
                    price=self.data.Close[-1],
                    cash=self._cash,
                    allocation_percentage=self._allocation_percentage / 2,
                ),
                tag=self._cash,
            )

        if self._is_bullish_reversal_on_short() and self.position.is_short:
            self.position.close()

        # pylint: enable=attribute-defined-outside-init


# pylint: enable=duplicate-code
