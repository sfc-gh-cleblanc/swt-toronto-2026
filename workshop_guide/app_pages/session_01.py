import streamlit as st
from pathlib import Path
from components import (
    render_session_header,
    render_sql_block,
    render_explanation,
    render_technologies_used,
    render_key_concepts,
    render_what_you_built,
)

_STATIC = Path(__file__).parent.parent / "static"


render_session_header(
    1,
    "Create Snowflake Objects",
    "5 min",
    "External Volume, Catalog Integration, and Catalog-Linked Database",
)

render_technologies_used([
    {
        "name": "External Volume",
        "description": "Tells Snowflake where Iceberg data files live in cloud storage and which IAM role to use. The credential layer between Snowflake and S3.",
        "icon": "cloud",
    },
    {
        "name": "Catalog Integration",
        "description": "Connects Snowflake to an external Iceberg catalog (AWS Glue) using the Iceberg REST Catalog API with SigV4 authentication.",
        "icon": "sync",
    },
    {
        "name": "Catalog-Linked Database",
        "description": "Auto-discovers and syncs every namespace and table from the Glue Data Catalog. No manual table registration needed.",
        "icon": "link",
    },
])

st.markdown("---")

st.markdown("#### Lab environment")
with st.container(border=True):
    st.markdown("""
The AWS infrastructure has been **pre-configured** for you. You do not need an AWS account or AWS credentials.

| Component | Value |
|-----------|-------|
| **S3 Bucket** | `s3://sf-lab-iceberg-484577546576/iceberg/` (us-east-2) |
| **Glue Database** | `iceberg` |
| **Iceberg Table** | `quotes` — ~56K insurance quote records in Iceberg V2 format |
| **IAM Role** | `arn:aws:iam::484577546576:role/sf-lab-shared-role` |
""")

st.markdown("---")

st.markdown("#### Open your workspace")
with st.container(border=True):
    st.markdown("""
Before running any SQL, open a workspace SQL file that you will reuse throughout this lab:

1. In the Snowsight left navigation, go to **Projects -> Workspaces**.
2. Select **My Workspace**, then click **+ Add new -> SQL file**.
3. Name the new file **`setup.sql`** and press Enter.

All of the SQL in this session will be run inside this `setup.sql` page.
""")
    col_nav, col_add = st.columns(2)
    with col_nav:
        st.image(str(_STATIC / "projects_workspaces_nav.png"), caption="Projects -> Workspaces in the left navigation")
    with col_add:
        st.image(str(_STATIC / "add_sql_file.png"), caption="My Workspace -> + Add new -> SQL file")

st.markdown("---")

render_sql_block(
    "1.1",
    "Create External Volume",
    """\
CREATE OR REPLACE EXTERNAL VOLUME my_iceberg_vol
  STORAGE_LOCATIONS = (
    (
      NAME             = 'us-east-2'
      STORAGE_PROVIDER = 'S3'
      STORAGE_BASE_URL = 's3://sf-lab-iceberg-484577546576/iceberg/'
      STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::484577546576:role/sf-lab-shared-role'
    )
  )
  ALLOW_WRITES = FALSE;""",
    "ALLOW_WRITES = FALSE marks this volume as read-only  --  Snowflake will not write back to S3.",
)

with st.container(border=True):
    st.markdown(
        ":material/lightbulb: **Tip: running SQL in your workspace file**  "
        "Click the **Run** button at the top left of the editor to execute your SQL. "
        "You can also use the keyboard shortcut **\u2318 + Return** (Mac) or **Ctrl + Enter** (Windows)."
    )
    st.image(str(_STATIC / "run_button.png"), width=400)

render_explanation("What is an External Volume?", """
An External Volume is the **credential and location layer** between Snowflake and your cloud object storage.
It tells Snowflake:
- **Where** the Iceberg data files live (the S3 bucket path)
- **How** to authenticate (the IAM role ARN)
- **What operations** are allowed (`ALLOW_WRITES = FALSE` for read-only)

Think of it as a named pointer to an S3 path with built-in IAM integration.
""")

st.write("")

render_sql_block(
    "1.2",
    "Create Catalog Integration",
    """\
CREATE OR REPLACE CATALOG INTEGRATION my_glue_int
  CATALOG_SOURCE = ICEBERG_REST
  TABLE_FORMAT   = ICEBERG
  REST_CONFIG = (
    CATALOG_URI      = 'https://glue.us-east-2.amazonaws.com/iceberg'
    CATALOG_API_TYPE = AWS_GLUE
    CATALOG_NAME     = '484577546576'
  )
  REST_AUTHENTICATION = (
    TYPE                 = SIGV4
    SIGV4_IAM_ROLE       = 'arn:aws:iam::484577546576:role/sf-lab-shared-role'
    SIGV4_SIGNING_REGION = 'us-east-2'
  )
  ENABLED = TRUE;""",
)

render_explanation("What is a Catalog Integration?", """
A Catalog Integration tells Snowflake how to reach an **external Iceberg catalog** — in this case,
the AWS Glue Iceberg REST Catalog (IRC) endpoint.

Key components:
- **CATALOG_SOURCE = ICEBERG_REST** — uses the open Iceberg REST API standard
- **CATALOG_API_TYPE = AWS_GLUE** — targets the Glue-specific IRC endpoint
- **SIGV4 authentication** — AWS Signature Version 4 signing using the shared IAM role
- **CATALOG_NAME** — the AWS account ID where the Glue catalog lives

This is how Snowflake discovers what tables exist in Glue without you manually registering each one.
""")

st.write("")

render_sql_block(
    "1.3",
    "Create Catalog-Linked Database",
    """\
CREATE OR REPLACE DATABASE my_iceberg_db
  LINKED_CATALOG = (
    CATALOG                  = 'my_glue_int',
    SYNC_INTERVAL_SECONDS    = 3600,
    ALLOWED_WRITE_OPERATIONS = NONE
  )
  EXTERNAL_VOLUME = 'my_iceberg_vol';""",
    "SYNC_INTERVAL_SECONDS = 3600 polls the catalog every hour. ALLOWED_WRITE_OPERATIONS = NONE enforces read-only.",
)

render_explanation("What is a Catalog-Linked Database?", """
A Catalog-Linked Database (CLD) is Snowflake's mechanism for **auto-discovering** and staying in sync
with external Iceberg catalogs.

Once created, Snowflake:
1. Connects to the Glue catalog via the Catalog Integration
2. Discovers all namespaces and tables
3. Makes them queryable as if they were native Snowflake tables
4. Re-syncs on the interval you specify (every hour in this lab)

**No manual `CREATE ICEBERG TABLE` or `ALTER TABLE ... REFRESH` needed.** When tables are added or
modified in Glue, Snowflake picks them up automatically on the next sync cycle.
""")

st.write("")

render_sql_block(
    "1.4",
    "Verify Sync",
    "SELECT SYSTEM$CATALOG_LINK_STATUS('my_iceberg_db');",
    'Look for "failureDetails":[] and "executionState":"RUNNING" or "SUCCEEDED" in the output. '
    "If you see failures, wait 30 seconds and re-run.",
)

render_explanation("How sync verification works", """
`SYSTEM$CATALOG_LINK_STATUS` returns a JSON payload describing the sync state. Key fields:

- **executionState** — `RUNNING` means syncing is in progress, `SUCCEEDED` means last sync completed
- **failureDetails** — empty array `[]` means no errors
- **lastSyncedAt** — timestamp of the most recent successful sync

The `quotes` table should appear within 60 seconds of creating the database. Once synced,
you can query it like any other Snowflake table.
""")

st.markdown("---")

render_key_concepts([
    {
        "term": "Apache Iceberg",
        "definition": "An open table format for large analytical datasets. Provides ACID transactions, schema evolution, and high-performance queries on data stored in object storage like S3. Both Snowflake and AWS support Iceberg natively.",
    },
    {
        "term": "Iceberg REST Catalog (IRC)",
        "definition": "An open API standard for managing Iceberg table metadata. AWS Glue exposes this API, allowing Snowflake to discover and read tables without proprietary connectors.",
    },
    {
        "term": "SigV4 Authentication",
        "definition": "AWS Signature Version 4 — the standard signing protocol for authenticating requests to AWS services. Snowflake uses SigV4 to securely communicate with the Glue IRC endpoint.",
    },
    {
        "term": "Catalog-Linked Database",
        "definition": "A Snowflake database that auto-discovers and syncs tables from an external Iceberg catalog. No manual table registration — Snowflake polls the catalog and keeps its local view current.",
    },
])

render_what_you_built([
    "my_iceberg_vol — External Volume pointing to the lab's S3 Iceberg data",
    "my_glue_int — Catalog Integration connecting to AWS Glue via Iceberg REST",
    "my_iceberg_db — Catalog-Linked Database auto-syncing tables from Glue",
    "Verified the quotes table is accessible from Snowflake",
])
