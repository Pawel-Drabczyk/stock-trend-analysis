SELECT
    reports.company_name,
    reports.symbol,
    reports.type,
    reports.description,
    reports.report_date,
    reports.dt,
    mapping.isin_code
FROM
    {{ ref('stg_finance_reports') }} reports
LEFT JOIN
    {{ ref('finance_reports_isin_mapping') }} mapping
USING
  (company_name)
