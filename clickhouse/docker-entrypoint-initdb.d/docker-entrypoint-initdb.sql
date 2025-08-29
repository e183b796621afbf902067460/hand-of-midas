-- Actual database to store the data
CREATE DATABASE IF NOT EXISTS clickhouse;

-- `Candlesticks` and `Smoothed Candlesticks` data
CREATE TABLE IF NOT EXISTS clickhouse.candlesticks
(
    exchange   String,
    section    String,
    ticker     String,
    interval   String,

    open       Float64,
    high       Float64,
    low        Float64,
    close      Float64,

    open_time  DateTime,
    close_time DateTime
)
ENGINE = MergeTree
PARTITION BY (
    exchange,
    section,
    ticker,
    interval,
    toYYYYMM(open_time)
)
ORDER BY (
    exchange,
    section,
    ticker,
    interval,
    open_time
);

CREATE TABLE IF NOT EXISTS clickhouse.smoothed_candlesticks
(
    exchange          String,
    section           String,
    ticker            String,
    interval          String,

    global_sma_open   Float64,
    global_sma_high   Float64,
    global_sma_low    Float64,
    global_sma_close  Float64,

    macro_trima_open  Float64,
    macro_trima_high  Float64,
    macro_trima_low   Float64,
    macro_trima_close Float64,

    macro_tema_open   Float64,
    macro_tema_high   Float64,
    macro_tema_low    Float64,
    macro_tema_close  Float64,

    micro_trima_open  Float64,
    micro_trima_high  Float64,
    micro_trima_low   Float64,
    micro_trima_close Float64,

    micro_tema_open   Float64,
    micro_tema_high   Float64,
    micro_tema_low    Float64,
    micro_tema_close  Float64,

    datetime          DateTime
)
ENGINE = MergeTree
PARTITION BY (
    exchange,
    section,
    ticker,
    interval,
    toYYYYMM(datetime)
)
ORDER BY (
    exchange,
    section,
    ticker,
    interval,
    datetime
);

-- `Booleans` and `Streaks` data
CREATE TABLE IF NOT EXISTS clickhouse.booleans
(
    exchange                                            String,
    section                                             String,
    ticker                                              String,
    interval                                            String,

    -- `Is Green Candle` data
    is_global_sma_close_greater_than_global_sma_open    Bool,
    is_macro_trima_close_greater_than_macro_trima_open  Bool,
    is_macro_tema_close_greater_than_macro_tema_open    Bool,
    is_micro_trima_close_greater_than_micro_trima_open  Bool,
    is_micro_tema_close_greater_than_micro_tema_open    Bool,

    -- `Is Upper SAR` data
    is_global_sma_low_greater_than_global_sma_sar       Bool,
    is_macro_trima_low_greater_than_macro_trima_sar     Bool,
    is_macro_tema_low_greater_than_macro_tema_sar       Bool,
    is_micro_trima_low_greater_than_micro_trima_sar     Bool,
    is_micro_tema_low_greater_than_micro_tema_sar       Bool,

    datetime                                            DateTime
)
ENGINE = MergeTree
PARTITION BY (
    exchange,
    section,
    ticker,
    interval,
    toYYYYMM(datetime)
)
ORDER BY (
    exchange,
    section,
    ticker,
    interval,
    datetime
);

CREATE TABLE IF NOT EXISTS clickhouse.streaks
(
    exchange                                                    String,
    section                                                     String,
    ticker                                                      String,
    interval                                                    String,

    -- `Green Candle Streak` data
    is_global_sma_close_greater_than_global_sma_open_streak     UInt256,
    is_macro_trima_close_greater_than_macro_trima_open_streak   UInt256,
    is_macro_tema_close_greater_than_macro_tema_open_streak     UInt256,
    is_micro_trima_close_greater_than_micro_trima_open_streak   UInt256,
    is_micro_tema_close_greater_than_micro_tema_open_streak     UInt256,

    -- `SAR Streak` data
    is_global_sma_low_greater_than_global_sma_sar_streak        Bool,
    is_macro_trima_low_greater_than_macro_trima_sar_streak      Bool,
    is_macro_tema_low_greater_than_macro_tema_sar_streak        Bool,
    is_micro_trima_low_greater_than_micro_trima_sar_streak      Bool,
    is_micro_tema_low_greater_than_micro_tema_sar_streak        Bool,

    datetime                                                    DateTime
)
ENGINE = MergeTree
PARTITION BY (
    exchange,
    section,
    ticker,
    interval,
    toYYYYMM(datetime)
)
ORDER BY (
    exchange,
    section,
    ticker,
    interval,
    datetime
);

-- `Indicators` data
CREATE TABLE IF NOT EXISTS clickhouse.sar
(
    exchange           String,
    section            String,
    ticker             String,
    interval           String,

    global_sma_sar     Float64,
    macro_trima_sar    Float64,
    macro_tema_sar     Float64,
    micro_trima_sar    Float64,
    micro_tema_sar     Float64,

    datetime           DateTime
)
ENGINE = MergeTree
PARTITION BY (
    exchange,
    section,
    ticker,
    interval,
    toYYYYMM(datetime)
)
ORDER BY (
    exchange,
    section,
    ticker,
    interval,
    datetime
);

CREATE TABLE IF NOT EXISTS clickhouse.rsi
(
    exchange                String,
    section                 String,
    ticker                  String,
    interval                String,

    global_sma_high_rsi     Float64,
    global_sma_low_rsi      Float64,
    global_sma_sar_rsi      Float64,

    macro_trima_high_rsi    Float64,
    macro_trima_low_rsi     Float64,
    macro_trima_sar_rsi     Float64,

    macro_tema_high_rsi     Float64,
    macro_tema_low_rsi      Float64,
    macro_tema_sar_rsi      Float64,

    micro_trima_high_rsi    Float64,
    micro_trima_low_rsi     Float64,
    micro_trima_sar_rsi     Float64,

    micro_tema_high_rsi     Float64,
    micro_tema_low_rsi      Float64,
    micro_tema_sar_rsi      Float64,

    datetime                DateTime
)
ENGINE = MergeTree
PARTITION BY (
    exchange,
    section,
    ticker,
    interval,
    toYYYYMM(datetime)
)
ORDER BY (
    exchange,
    section,
    ticker,
    interval,
    datetime
);
