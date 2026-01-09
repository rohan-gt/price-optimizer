### Natural language query example

Show total net revenue in USD by customer country and signup month for paid users in the last quarter, where net revenue is payment amount minus tax, and customers are joined using a derived customer key. Include only customers whose lifetime spend exceeds 1000 USD.

---

### SQL query solution using joins, transformations, and aggregations

```sql
WITH transformed_payments AS (
  SELECT
    p.payment_id,
    p.customer_id,
    p.created_at,
    (p.amount - p.tax_amount) AS net_amount_usd
  FROM payments p
  WHERE p.user_type = 'paid'
    AND p.created_at BETWEEN DATE '2024-10-01' AND DATE '2024-12-31'
),
customer_lifetime AS (
  SELECT
    customer_id,
    SUM(amount - tax_amount) AS lifetime_spend
  FROM payments
  GROUP BY customer_id
),
eligible_customers AS (
  SELECT
    c.customer_id,
    c.country,
    DATE_TRUNC('month', c.signup_date) AS signup_month
  FROM customers c
  JOIN customer_lifetime cl
    ON c.customer_id = cl.customer_id
  WHERE cl.lifetime_spend > 1000
)
SELECT
  ec.country,
  ec.signup_month,
  SUM(tp.net_amount_usd) AS total_net_revenue_usd
FROM transformed_payments tp
JOIN eligible_customers ec
  ON tp.customer_id = ec.customer_id
GROUP BY ec.country, ec.signup_month
ORDER BY total_net_revenue_usd DESC;
```

This query uses:
- joins between fact and dimension tables
- a transformation computing net revenue
- an aggregation over a transformed metric
- a derived aggregation used as a filter
- time filtering and grouping
- a derived join key path through CTEs

---

### Notes on identifiers and names

All entities use two distinct concepts:
- **id** is a stable generated identifier used for lineage, graph edges, and internal references
- **name** is the human readable object name as it exists in the database or business layer

IDs do not change even if names change.

---

### Updated metadata tables with name fields added everywhere

### `databases`

| Column | Type | Description | Example Value |
|------|------|-------------|---------------|
| database_id | TEXT | Generated unique identifier for the database | db_001 |
| name | TEXT | Human readable database name | analytics_db |
| description | TEXT | Natural language description used for search and embeddings | Primary analytics database containing business data |
| created_at | TIMESTAMPTZ | Timestamp when the database was created | 2024-01-01 |

---

### `schemas`

| Column | Type | Description | Example Value |
|------|------|-------------|---------------|
| schema_id | TEXT | Generated unique identifier for the schema | sch_001 |
| database_id | TEXT | Identifier of the database this schema belongs to | db_001 |
| name | TEXT | Human readable schema name | public |
| description | TEXT | Natural language description used for search and embeddings | Core schema containing business tables |

---

### `tables`

| Column | Type | Description | Example Value |
|------|------|-------------|---------------|
| table_id | TEXT | Generated unique identifier for the table | tbl_payments |
| schema_id | TEXT | Identifier of the schema this table belongs to | sch_001 |
| name | TEXT | Human readable table name | payments |
| description | TEXT | Natural language description used for search and embeddings | Table storing individual payment transactions |
| type | TEXT | Classification of table as fact or dimension | fact |
| updated_at | TIMESTAMPTZ | Timestamp when the table was last updated | 2024-12-31 |
| primary_key | TEXT | Identifier of the primary key column | col_payment_id |

---

### `columns`

| Column | Type | Description | Example Value |
|------|------|-------------|---------------|
| column_id | TEXT | Generated unique identifier for the column | col_amount |
| table_id | TEXT | Identifier of the table this column belongs to | tbl_payments |
| name | TEXT | Human readable column name | amount |
| description | TEXT | Natural language description used for search and embeddings | Monetary amount of a payment |
| data_type | TEXT | Data type of the column | numeric |
| semantic_type | TEXT | Semantic classification of the column | metric |
| unique_values_count | BIGINT | Estimated number of distinct values | 100000 |
| numeric_stats | JSONB | Summary statistics for numeric columns | {"min":1,"max":5000} |
| example_values | TEXT[] | Example values observed in the column | {19.99,49.99} |
| nullable | BOOLEAN | Indicates whether null values are allowed | false |

---

### `transformations`

| Column | Type | Description | Example Value |
|------|------|-------------|---------------|
| transformation_id | TEXT | Generated unique identifier for the transformation | tr_net_revenue |
| name | TEXT | Human readable transformation name | net_revenue_usd |
| expression | TEXT | Expression defining how the transformation is computed | amount minus tax_amount |
| description | TEXT | Natural language description used for search and embeddings | Net payment revenue after tax |
| created_by | TEXT | Identifier of the creator | finance_etl |
| created_at | TIMESTAMPTZ | Timestamp when the transformation was created | 2024-06-01 |

---

### `transformation_columns`

| Column | Type | Description | Example Value |
|------|------|-------------|---------------|
| transformation_id | TEXT | Identifier of the transformation | tr_net_revenue |
| column_id | TEXT | Identifier of a column used by the transformation | col_amount |

---

### `aggregations`

| Column | Type | Description | Example Value |
|------|------|-------------|---------------|
| agg_id | TEXT | Generated unique identifier for the aggregation | agg_total_net_revenue |
| name | TEXT | Human readable aggregation name | total_net_revenue |
| description | TEXT | Natural language description used for search and embeddings | Total net revenue summed across payments |
| agg_type | TEXT | Type of aggregation operation | sum |
| base_column_ids | TEXT[] | Identifiers of columns used directly | {} |
| base_transformation_ids | TEXT[] | Identifiers of transformations used | {tr_net_revenue} |

---

### `joins`

| Column | Type | Description | Example Value |
|------|------|-------------|---------------|
| join_id | TEXT | Generated unique identifier for the join | join_payments_customers |
| name | TEXT | Human readable join name | payments_to_customers |
| left_entity_id | TEXT | Identifier of the left column or transformation | col_customer_id |
| right_entity_id | TEXT | Identifier of the right column or transformation | col_customer_id |
| join_type | TEXT | Classification of join as foreign key inferred or derived | FK |
| confidence_score | REAL | Numeric confidence score between zero and one indicating join reliability | 1.0 |
| description | TEXT | Natural language description used for search and embeddings | Relationship connecting payments to customers using customer identifiers |
