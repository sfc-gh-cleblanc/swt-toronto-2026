import streamlit as st
from components import (
    render_session_header,
    render_coco_prompt,
    render_explanation,
    render_technologies_used,
    render_key_concepts,
    render_what_you_built,
)

render_session_header(
    4,
    "Semantic View",
    "10 min",
    "Business metrics and dimensions for AI-ready analytics on Iceberg data",
)

render_technologies_used([
    {
        "name": "Semantic View",
        "description": "Defines the business meaning of your data — dimensions, metrics, and facts — so Snowflake's AI can understand and query it in natural language.",
        "icon": "schema",
    },
    {
        "name": "Cortex Analyst",
        "description": "Snowflake's natural language to SQL engine. Uses the semantic view to translate plain English questions into accurate SQL queries.",
        "icon": "translate",
    },
    {
        "name": "Masking Pass-Through",
        "description": "The semantic view respects masking policies automatically — an analyst querying via natural language sees the same masked values as in direct SQL.",
        "icon": "shield",
    },
])

st.markdown("---")

st.markdown("""
A Semantic View defines the **business meaning** of your data — dimensions, metrics, and facts — so
that Snowflake's AI can understand and answer questions about it in natural language.

The semantic view sits on top of `quotes_vw` (the view wrapper from Session 3), so masking
policies are enforced automatically. An analyst querying via natural language sees the same
masked values as they would in direct SQL.
""")

st.write("")

render_coco_prompt(
    "4.1",
    "Create Semantic View",
    "Create a new worksheet for the semantic view. "
    "In iceberg_lab_db.analytics, create a semantic view called quotes_sv on top of quotes_vw with uuid as the primary key.\n\n"
    "Facts: newriskpremium (risk premium), totalpremiumpayable (total premium), iptamount (insurance premium tax), "
    "and a quote_record fact set to 1 for counting.\n\n"
    "Dimensions: quote_product (synonyms: product type, insurance product, cover type, policy type), "
    "quotedate (synonyms: quote date, date, when requested), "
    "maritalstatus (synonyms: marital status, married, single), "
    "homeownerind (synonyms: homeowner, owns home, property owner), "
    "sex (synonyms: gender, customer gender), "
    "postcodedistrict (synonyms: district, location, area, region, province, postal district), "
    "previnsr (synonyms: previous insurer, prior insurer, prior provider).\n\n"
    "Metrics: total_quotes (COUNT of quote_record), avg_total_premium (AVG totalpremiumpayable), "
    "avg_risk_premium (AVG newriskpremium), total_premium_volume (SUM totalpremiumpayable).\n\n"
    "Add a comment: 'Insurance quote analytics on Iceberg data in AWS Glue via Catalog-Linked Database'.",
    sql="""\
USE ROLE ACCOUNTADMIN;
USE DATABASE iceberg_lab_db;
USE SCHEMA analytics;

CREATE OR REPLACE SEMANTIC VIEW quotes_sv
  TABLES (
    quotes as quotes_vw
      primary key (UUID)
      comment='Insurance quote requests from the Iceberg data lake in AWS Glue'
  )
  FACTS (
    quotes.NEWRISKPREMIUM      as NEWRISKPREMIUM      comment='Calculated risk premium',
    quotes.TOTALPREMIUMPAYABLE as TOTALPREMIUMPAYABLE comment='Total premium payable',
    quotes.IPTAMOUNT           as IPTAMOUNT           comment='Insurance premium tax',
    quotes.QUOTE_RECORD        as 1                   comment='One record per quote'
  )
  DIMENSIONS (
    quotes.QUOTE_PRODUCT    as QUOTE_PRODUCT    with synonyms=('product type', 'insurance product', 'cover type', 'policy type') comment='Insurance product type',
    quotes.QUOTEDATE        as QUOTEDATE        with synonyms=('quote date', 'date', 'when requested')             comment='Date the quote was requested',
    quotes.MARITALSTATUS    as MARITALSTATUS    with synonyms=('marital status', 'married', 'single')              comment='Customer marital status',
    quotes.HOMEOWNERIND     as HOMEOWNERIND     with synonyms=('homeowner', 'owns home', 'property owner')         comment='Whether customer owns home',
    quotes.SEX              as SEX              with synonyms=('gender', 'customer gender')                        comment='Customer gender',
    quotes.POSTCODEDISTRICT as POSTCODEDISTRICT with synonyms=('district', 'location', 'area', 'region', 'province', 'postal district') comment='Customer postcode district',
    quotes.PREVINSR         as PREVINSR         with synonyms=('previous insurer', 'prior insurer', 'prior provider')                   comment='Previous insurance provider'
  )
  METRICS (
    quotes.total_quotes         as COUNT(quotes.QUOTE_RECORD)      comment='Total number of quote requests',
    quotes.avg_total_premium    as AVG(quotes.TOTALPREMIUMPAYABLE)  comment='Average total premium payable',
    quotes.avg_risk_premium     as AVG(quotes.NEWRISKPREMIUM)       comment='Average risk premium',
    quotes.total_premium_volume as SUM(quotes.TOTALPREMIUMPAYABLE)  comment='Total premium volume'
  )
  comment='Insurance quote analytics on Iceberg data in AWS Glue via Catalog-Linked Database';""",
)

render_explanation("How the semantic view works", """
The semantic view uses a **table alias mapping**: `quotes as quotes_vw` — where `quotes` is the
internal reference name and `quotes_vw` is the physical view. All column references use the
reference name `quotes`.

**Key components:**

- **FACTS** — numeric columns used for aggregation (premiums, tax, record count)
- **DIMENSIONS** — categorical columns for grouping and filtering (product, date, status)
- **METRICS** — pre-defined calculations (COUNT, AVG, SUM) that the AI can use directly
- **SYNONYMS** — alternative names the AI recognizes (e.g. "province" maps to postcodedistrict)

The `quote_record as 1` fact is a pattern for creating a countable record marker — every row
contributes 1 to the `total_quotes` metric.
""")

st.write("")

render_coco_prompt(
    "4.2",
    "Grant Access",
    "Grant both lab_analyst and lab_data_engineer access to iceberg_lab_db.analytics — "
    "they need USAGE on the database and schema, SELECT on quotes_vw, and SELECT on the semantic view quotes_sv.",
    sql="""\
GRANT USAGE ON DATABASE iceberg_lab_db TO ROLE lab_analyst;
GRANT USAGE ON SCHEMA iceberg_lab_db.analytics TO ROLE lab_analyst;
GRANT SELECT ON VIEW iceberg_lab_db.analytics.quotes_vw TO ROLE lab_analyst;
GRANT SELECT ON SEMANTIC VIEW iceberg_lab_db.analytics.quotes_sv TO ROLE lab_analyst;

GRANT USAGE ON DATABASE iceberg_lab_db TO ROLE lab_data_engineer;
GRANT USAGE ON SCHEMA iceberg_lab_db.analytics TO ROLE lab_data_engineer;
GRANT SELECT ON VIEW iceberg_lab_db.analytics.quotes_vw TO ROLE lab_data_engineer;
GRANT SELECT ON SEMANTIC VIEW iceberg_lab_db.analytics.quotes_sv TO ROLE lab_data_engineer;""",
)

st.write("")

render_coco_prompt(
    "4.3",
    "Verify Semantic View",
    "Verify the semantic view by running SHOW SEMANTIC VIEWS, SHOW SEMANTIC METRICS, and SHOW SEMANTIC DIMENSIONS "
    "for iceberg_lab_db.analytics.quotes_sv.",
    sql="""\
SHOW SEMANTIC VIEWS IN SCHEMA iceberg_lab_db.analytics;
SHOW SEMANTIC METRICS IN iceberg_lab_db.analytics.quotes_sv;
SHOW SEMANTIC DIMENSIONS IN iceberg_lab_db.analytics.quotes_sv;""",
    note="You should see 4 metrics and 7 dimensions.",
)

render_explanation("Verifying your semantic view", """
The three SHOW commands confirm:

1. **SHOW SEMANTIC VIEWS** — the `quotes_sv` view exists in `iceberg_lab_db.analytics`
2. **SHOW SEMANTIC METRICS** — all 4 pre-defined metrics are registered
3. **SHOW SEMANTIC DIMENSIONS** — all 7 dimensions with their synonyms are registered

Once verified, the semantic view is ready to power the Cortex Agent in Session 5.
The AI will use these definitions to translate natural language questions into accurate SQL.
""")

st.markdown("---")

st.markdown("#### :material/explore: 4.4 — Explore the Semantic View in Snowsight")

with st.container(border=True):
    st.markdown("""
Open the semantic view in the Snowsight UI to browse its dimensions, facts, and metrics,
then try a question in the built-in playground.

1. In the Snowsight left nav, click **Analyst → Semantic Views**
2. Find **QUOTES_SV** in the `ICEBERG_LAB_DB.ANALYTICS` schema and click to open it
3. Browse the **Dimensions** tab — you should see 7 dimensions including `quote_product`, `postcodedistrict`, and `maritalstatus` with their synonyms
4. Browse the **Facts & Metrics** tab — you should see 4 facts and 4 pre-defined metrics including `total_quotes` and `avg_total_premium`
5. Click the **Playground** tab at the top of the semantic view
6. Type the following question in the chat input and press Enter:

> *What are the top 5 insurance products by number of quotes?*

The playground will generate SQL from your question using the semantic view definitions and show the results.
    """)

st.write("")


render_key_concepts([
    {
        "term": "Semantic View",
        "definition": "A Snowflake object that overlays business meaning on top of physical tables. Defines facts (numeric columns), dimensions (categorical columns), and metrics (pre-defined calculations). Enables AI to understand and query data in natural language.",
    },
    {
        "term": "Synonyms",
        "definition": "Alternative names for dimensions that the AI recognizes. For example, 'province' and 'postal district' both map to the postcodedistrict column. Improves natural language query accuracy.",
    },
    {
        "term": "Cortex Analyst",
        "definition": "Snowflake's natural language to SQL engine. Uses the semantic view to understand data structure, then generates verified SQL from plain English questions. Results respect all governance policies.",
    },
])

render_what_you_built([
    "quotes_sv — Semantic View with 4 facts, 7 dimensions, and 4 metrics",
    "Canadian-friendly synonyms for natural language querying",
    "Grants for both lab roles to query via AI",
    "Verified metrics and dimensions are registered correctly",
    "Explored the semantic view in Snowsight and tested a natural language question in the playground",
])
