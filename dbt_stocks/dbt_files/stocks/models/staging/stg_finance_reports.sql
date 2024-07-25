SELECT
    company_name,
    symbol,
    type,
    description,
    CAST(report_date AS DATE) AS report_date,
    dt
FROM
    {{ source('finance_reports', 'finance_reports') }}
