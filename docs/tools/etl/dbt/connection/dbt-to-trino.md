# Trino

`dbt-trino` adapter uses Trino as a underlying query engine to perform query
federation across disperse data sources.
Trino connects to multiple and diverse data sources (available connectors) via
one dbt connection and process SQL queries at scale.
Transformations defined in dbt are passed to Trino which handles these SQL
transformation queries and translates them to queries specific to the systems it
connects to create tables or views and manipulate data.

## Prerequisite

### Configuring postgresql and trino

```yaml titles="docker-compose.yml"
version: '3.7'
services:
    sales:
        image: postgres:11
        container_name: sales
        restart: always
        environment:
            POSTGRES_DB: postgres
            POSTGRES_USER: postgres
            POSTGRES_PASSWORD: postgres
        ports:
            - "15432:5432"
        volumes:
            - ./postgres-data:/var/lib/postgresql/data
            - ./sql/create_tables.sql:/docker-entrypoint-initdb.d/create_tables.sql
            - ./sql/fill_tables.sql:/docker-entrypoint-initdb.d/fill_tables.sql
    trino:
        hostname: trino
        container_name: trino
        image: 'trinodb/trino:latest'
        ports:
            - '8080:8080'
        volumes:
            - ./catalog:/etc/trino/catalog
networks:
    trino-network:
        driver: bridge
```

Notice that we have a persisted volume inside a `catalog` folder.
Inside this folder, we need to set some configuration files to allow `trino` to
connect to our databases. In our case, we need to file, one for `postgres` and
the other for `bigquery`.

=== "Postgres"

    ```text titles="postgres.properties"
    connector.name=postgresql
    connection-url=jdbc:postgresql://sales:5432/postgres
    connection-user=postgres
    connection-password=postgres
    ```

=== "BigQuery"

    ```text titles="bigquery.properties"
    connector.name=bigquery
    bigquery.project-id=dbt-sales
    bigquery.views-enabled=false
    bigquery.credentials-file=/etc/trino/catalog/dbt-sales-svc.json
    ```

```shell
pip install dbt-trino dbt-bigquery
```

## References

- [Using dbt-trino as a data ingestion tool: Part I](https://medium.com/@joaopaulonobregaalvim/using-dbt-trino-as-a-data-ingestion-tool-part-i-43d172069285)
