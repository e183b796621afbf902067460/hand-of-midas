-- Actual database to store the data
CREATE DATABASE IF NOT EXISTS clickhouse;

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
