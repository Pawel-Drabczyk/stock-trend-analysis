FROM ghcr.io/dbt-labs/dbt-bigquery:1.7.2

COPY dbt_stocks/dbt_files /app_dependencies/dbt_files
COPY dbt_stocks/entrypoint.sh /app_dependencies/entrypoint.sh
COPY dbt_stocks/profiles.yml /app_dependencies/profiles.yml

WORKDIR /app_dependencies/dbt_files/stocks
RUN dbt deps --profiles-dir /app_dependencies


RUN chmod +x /app_dependencies/entrypoint.sh
ENTRYPOINT ["/app_dependencies/entrypoint.sh"]
