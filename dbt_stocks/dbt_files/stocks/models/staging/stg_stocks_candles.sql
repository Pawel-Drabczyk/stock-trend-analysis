SELECT
    Name AS name,
    ISIN_Code AS isin_code,
    Currency AS currency,
    CAST(Open_Price AS FLOAT64) AS open_price,
    CAST(High_Price AS FLOAT64) AS high_price,
    CAST(Low_Price AS FLOAT64) AS low_price,
    CAST(Close_Price AS FLOAT64) AS close_price,
    CAST(Price_Change____ AS FLOAT64) AS price_change,
    Volume AS volume,
    CAST(Transaction_Count AS INT) AS transaction_count,
    CAST(Turnover__k_ AS FLOAT64) AS turnover,
    Date AS date,
    dt
FROM
    {{ source('stocks_candles', 'stocks_candles') }}
