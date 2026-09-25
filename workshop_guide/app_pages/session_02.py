import streamlit as st
from pathlib import Path
from components import (
    render_session_header,
    render_coco_prompt,
    render_explanation,
    render_technologies_used,
    render_key_concepts,
    render_what_you_built,
)

_STATIC = Path(__file__).parent.parent / "static"

render_session_header(
    2,
    "Query Iceberg Data",
    "10 min",
    "SQL queries against Iceberg tables in AWS Glue — zero data movement",
)

render_technologies_used([
    {
        "name": "Catalog-Linked Database",
        "description": "Query external Iceberg tables exactly like native Snowflake tables. Data is read directly from S3 — nothing is copied.",
        "icon": "link",
    },
    {
        "name": "Case-Sensitive Identifiers",
        "description": "AWS Glue uses lowercase identifiers. Schema and table names must be wrapped in double quotes when querying a CLD.",
        "icon": "format_quote",
    },
    {
        "name": "Zero-Copy Analytics",
        "description": "Snowflake reads Iceberg data files directly from S3 using the External Volume. No data movement, no storage duplication.",
        "icon": "cloud_download",
    },
])

st.markdown("---")

st.info(
    '**Heads up:** AWS Glue uses case-insensitive, lowercase identifiers. '
    'Always wrap schema and table names in double quotes when querying a '
    'Catalog-Linked Database — e.g. `my_iceberg_db."iceberg"."quotes"`.'
)

st.write("")

render_coco_prompt(
    "2.1",
    "Explore the Table",
    "Create a blank sql sheet if the current one isn't blank. Add the necessary SQL to show me the first 10 rows from the quotes table in my_iceberg_db and give me the total row count. "
    "Remember to set context for the sheet and note that the schema and table names are lowercase in Glue so ensure to use double quotes like "
    '"iceberg"."quotes".',
    sql="""\
-- Preview the first 10 rows
SELECT * FROM my_iceberg_db."iceberg"."quotes" LIMIT 10;

-- Check the total row count
SELECT COUNT(*) AS total_quotes FROM my_iceberg_db."iceberg"."quotes";""",
    note="You should see approximately 56,000 quote records.",
)

with st.container(border=True):
    st.markdown(
        ":material/lightbulb: **Tip: opening CoCo**  "
        "Click the blue **CoCo button** in the bottom-right corner of the Snowsight window to open the CoCo chat panel."
    )
    st.image(str(_STATIC / "coco_button.png"), width=150)

render_explanation("What just happened?", """
You queried an **Apache Iceberg table stored in AWS S3** directly from Snowflake — without copying
any data. Snowflake:

1. Used the **External Volume** to locate and read Parquet data files in S3
2. Used the **Catalog Integration** to resolve the table's metadata from AWS Glue
3. Returned the results as if this were a native Snowflake table

The `quotes` table contains ~56K insurance quote requests with 40 columns including customer details,
policy information, and pricing attributes.
""")

st.write("")

render_coco_prompt(
    "2.2",
    "Quote Volume by Product",
    "Query my_iceberg_db to show quote volume by product type — count of quotes and average total premium payable per product, "
    "ordered by volume descending.",
    sql="""\
SELECT
    quote_product,
    COUNT(*)                           AS total_quotes,
    ROUND(AVG(totalpremiumpayable), 2) AS avg_premium
FROM my_iceberg_db."iceberg"."quotes"
GROUP BY quote_product
ORDER BY total_quotes DESC;""",
    note="Shows which insurance products generate the most quote activity and their average premiums.",
)

render_explanation("Insurance product analytics", """
This query reveals the **product mix** across all quote requests. In Canadian insurance markets,
common product types include home, auto, travel, and life insurance.

The `avg_premium` metric shows the average `totalpremiumpayable` per product — useful for
identifying high-value product lines and understanding pricing distribution across the portfolio.
""")

st.write("")

render_coco_prompt(
    "2.3",
    "High-Frequency Customers",
    "Find customers in my_iceberg_db who requested more than one quote. Show their surname, postcode district, "
    "quote count, first and last quote dates, and average premium. Order by quote count descending, limit to 20.",
    sql="""\
SELECT
    surname,
    postalcode,
    COUNT(*)                           AS quote_count,
    MIN(quotedate)                     AS first_quote,
    MAX(quotedate)                     AS last_quote,
    ROUND(AVG(totalpremiumpayable), 2) AS avg_premium
FROM my_iceberg_db."iceberg"."quotes"
GROUP BY surname, postalcode
HAVING COUNT(*) > 1
ORDER BY quote_count DESC
LIMIT 20;""",
    note="Identifies customers who requested multiple quotes — a key signal for churn risk in insurance.",
)

render_explanation("Why high-frequency quoting matters", """
Customers who request **multiple quotes** in a short window are often comparison-shopping — a strong
signal for potential churn in the insurance industry.

This pattern is especially relevant for Canadian insurers where provincial regulations
affect pricing and customers frequently shop across providers. The `postalcode` column
helps identify geographic clusters of high-frequency quoters.
""")

st.write("")

render_coco_prompt(
    "2.4",
    "Premium by Credit Score Band",
    "Group the quotes in my_iceberg_db into three credit score bands: High (8-10), Medium (5-7), and Low (0-4). "
    "For each band show the quote count, average risk premium, and average total premium. Order by average risk premium descending.",
    sql="""\
SELECT
    CASE
        WHEN creditscore >= 8 THEN 'High (8-10)'
        WHEN creditscore >= 5 THEN 'Medium (5-7)'
        ELSE 'Low (0-4)'
    END                                AS credit_band,
    COUNT(*)                           AS quote_count,
    ROUND(AVG(newriskpremium), 2)      AS avg_risk_premium,
    ROUND(AVG(totalpremiumpayable), 2) AS avg_total_premium
FROM my_iceberg_db."iceberg"."quotes"
GROUP BY credit_band
ORDER BY avg_risk_premium DESC;""",
    note="Shows how credit scores correlate with insurance risk premiums.",
)

render_explanation("Credit score and risk pricing", """
Insurance risk pricing often correlates with credit scores — a pattern well-documented in
North American insurance markets. This query groups customers into three credit bands and
compares their average premiums.

Key metrics:
- **avg_risk_premium** — the calculated risk component of the premium
- **avg_total_premium** — the final amount payable including all fees and taxes

In regulated Canadian markets, insurers must justify premium differentials based on actuarial
data. This analysis helps validate that credit-based pricing follows expected patterns.
""")

st.markdown("---")

render_key_concepts([
    {
        "term": "Zero-Copy Querying",
        "definition": "Snowflake reads Iceberg data files directly from S3 via the External Volume. No data is copied into Snowflake storage — you pay only for compute, not duplicate storage.",
    },
    {
        "term": "Double-Quoted Identifiers",
        "definition": 'AWS Glue uses lowercase identifiers. In Snowflake SQL, wrap them in double quotes (e.g. "iceberg"."quotes") to preserve case sensitivity when querying a CLD.',
    },
    {
        "term": "Iceberg V2 Format",
        "definition": "Apache Iceberg V2 adds row-level deletes and position delete files on top of V1's partition evolution and schema evolution. The quotes table uses V2 format.",
    },
])

render_what_you_built([
    "Confirmed the quotes Iceberg table is queryable from Snowflake",
    "Analyzed quote volume by insurance product type",
    "Identified high-frequency customers as churn risk signals",
    "Explored premium distribution across credit score bands",
])
