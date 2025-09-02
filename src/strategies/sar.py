from src.strategies.common.sar_base import BearishSARStrategy, BullishSARStrategy


class MixinSARStrategy(BullishSARStrategy, BearishSARStrategy):
    def init(self) -> None:
        BullishSARStrategy.init(self)
        BearishSARStrategy.init(self)

    def next(self) -> None:
        BullishSARStrategy.next(self)
        BearishSARStrategy.next(self)
