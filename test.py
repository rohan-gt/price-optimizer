### Natural language query example

Show total net revenue in USD by customer country and signup month for paid users in the last quarter, where net revenue is payment amount minus tax, only include customers whose lifetime spend is greater than 1000 USD, and keep customers even if they have no payments in the period.

---

### SQL query solution

```sql
WITH transformed_payments AS (
  SELECT
    p.payment_id,
    p.customer_id,
    p.created_at,
    (p.amount - p.tax_amount) AS net_revenue_usd
  FROM payments p
  WHERE p.user_type = 'paid'
    AND p.created_at BETWEEN DATE '2024-10-01' AND DATE '2024-12-31'
),
customer_lifetime AS (
  SELECT
    customer_id,
    SUM(amount - tax_amount) AS lifetime_spend_usd
  FROM payments
  GROUP BY customer_id
),
eligible_customers AS (
  SELECT
    c.customer_id,
    c.country,
    DATE_TRUNC('month', c.signup_date) AS signup_month
  FROM customers c
  LEFT JOIN customer_lifetime cl
    ON c.customer_id = cl.customer_id
  WHERE cl.lifetime_spend_usd > 1000
)
SELECT
  ec.country,
  ec.signup_month,
  SUM(tp.net_revenue_usd) AS total_net_revenue_usd
FROM eligible_customers ec
LEFT JOIN transformed_payments tp
  ON ec.customer_id = tp.customer_id
GROUP BY ec.country, ec.signup_month
ORDER BY total_net_revenue_usd DESC;
```

This query uses:
- multiple CTE subqueries
- transformations
- aggregations on transformations
- filters at different stages
- left joins to preserve dimension rows
- unit aware metrics

---

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
| unit | TEXT | Unit or currency of the column values | USD |
| top_values | JSONB | Top values by frequency for categorical data | null |
| quartiles | JSONB | Quartile values for numeric data | {"p25":100,"p50":300,"p75":800} |
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
| name | TEXT | Human readable join name | payments_customers |
| left_entity_id | TEXT | Identifier of the left column or transformation | col_customer_id |
| right_entity_id | TEXT | Identifier of the right column or transformation | col_customer_id |
| join_type | TEXT | Join type such as inner left right or full | left |
| confidence_score | REAL | Numeric confidence score between zero and one | 1.0 |
| description | TEXT | Natural language description used for search and embeddings | Join between payments and customers on customer identifier |

---

### `filters`

| Column | Type | Description | Example Value |
|------|------|-------------|---------------|
| filter_id | TEXT | Generated unique identifier for the filter | fl_paid_users |
| entity_id | TEXT | Identifier of the column or transformation filtered | col_user_type |
| operator | TEXT | Filter operator | equals |
| value | TEXT | Filter comparison value | paid |
| description | TEXT | Natural language description used for search and embeddings | Filter to include only paid users |

---

### `subqueries`

| Column | Type | Description | Example Value |
|------|------|-------------|---------------|
| subquery_id | TEXT | Generated unique identifier for the subquery | sq_customer_lifetime |
| name | TEXT | Human readable subquery name | customer_lifetime |
| description | TEXT | Natural language description used for search and embeddings | Computes lifetime spend per customer |
| sql_logic | TEXT | SQL logic defining the subquery | sum of payment amounts grouped by customer |
| used_as | TEXT | How the subquery is used | cte |
