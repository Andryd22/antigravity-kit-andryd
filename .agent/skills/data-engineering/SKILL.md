---
name: data-engineering
description: Data pipeline design, ETL/ELT patterns, orchestration, data warehousing, and data quality. Covers Airflow, dbt, Spark, and streaming architectures.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Data Engineering

> Build reliable data pipelines. Move data from source to insight. Test everything.

## Pipeline Patterns

### Batch ETL
```
Extract (API/DB) → Transform (dbt/Spark) → Load (Warehouse)
Schedule: hourly/daily, idempotent, partition-aware
```

### Streaming ETL
```
Event (Kafka/PubSub) → Transform (Flink/Spark Streaming) → Sink (Warehouse/Lake)
Latency: seconds, at-least-once or exactly-once semantics
```

### ELT (Modern)
```
Extract → Load (raw to warehouse) → Transform (dbt SQL inside warehouse)
Why: Warehouse compute is cheap, raw data preserved for reprocessing
```

## Orchestration

| Tool | Best For | Trade-off |
|------|----------|-----------|
| **Airflow** | Complex DAGs, enterprise | Heavy infra, steep learning |
| **Prefect** | Python-native, modern | Smaller community |
| **Dagster** | Asset-based, testing | Newer ecosystem |
| **dbt Cloud** | SQL transforms only | Limited to data modeling |

### Scheduling Principles
```python
# ✅ Idempotent: run multiple times, same result
INSERT INTO users_clean
SELECT DISTINCT ON (id) * FROM raw_users
WHERE ingested_at > '{{ ds }}';

# ❌ Not idempotent: doubles on re-run
INSERT INTO users_clean SELECT * FROM raw_users;
```

## Data Modeling

### Dimensional (Star Schema)
```
fact_sales (date_key, product_key, customer_key, amount, quantity)
├── dim_date (date_key, day, month, year, is_holiday)
├── dim_product (product_key, name, category, price)
└── dim_customer (customer_key, name, segment, region)
```

### dbt Patterns
```sql
-- models/staging/stg_orders.sql
WITH source AS (
    SELECT * FROM {{ source('raw', 'orders') }}
),
cleaned AS (
    SELECT
        id AS order_id,
        user_id,
        amount_cents / 100.0 AS amount_dollars,
        status,
        created_at::date AS order_date
    FROM source
    WHERE status != 'test'
)
SELECT * FROM cleaned
```

## Data Quality

| Check | Tool | Example |
|-------|------|---------|
| **Not null** | dbt test / Great Expectations | `not_null: order_id` |
| **Uniqueness** | dbt test | `unique: order_id` |
| **Freshness** | dbt source freshness | `warn_after: {count: 1, period: hour}` |
| **Referential** | dbt relationships | `relationships: orders.customer_id → customers.id` |
| **Distribution** | Great Expectations | Column mean within expected range |

## Storage Layer

| Layer | Purpose | Retention |
|-------|---------|-----------|
| **Raw/Bronze** | Immutable source copy | Forever (cheap storage) |
| **Cleaned/Silver** | Deduped, typed, joined | 90 days rolling |
| **Aggregated/Gold** | Business metrics, KPI tables | Policy-dependent |

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| `SELECT *` in production | Explicit column list |
| No partition pruning | Filter by partition key in WHERE |
| Single monolithic DAG | Modular DAGs with clear dependencies |
| Skip backfill planning | Design for backfill from day 1 |
| No retry logic | Exponential backoff, dead-letter queue |
| Silent data quality failures | Alert on freshness, null rate spikes |

## Checklist

- [ ] Pipeline is idempotent (safe to re-run)
- [ ] Source data has freshness monitoring
- [ ] Incremental models have unique_key defined
- [ ] dbt tests cover not_null, unique, relationships
- [ ] Backfill plan documented and tested
- [ ] Sensitive columns identified (PII, secrets)
- [ ] CI pipeline runs `dbt test` on PR
