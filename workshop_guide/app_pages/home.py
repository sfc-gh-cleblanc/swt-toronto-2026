import streamlit as st
from pathlib import Path

_STATIC = Path(__file__).parent.parent / "static"

col_logo, col_leaf = st.columns([1, 1])
with col_logo:
    st.image(str(_STATIC / "snowflake_world_tour.png"), width=172)
with col_leaf:
    st.image(str(_STATIC / "maple_leaf.jpg"), width=150)

st.title("Power Analytics and AI Wherever Your Data Lives")
st.markdown("Snowflake World Tour Toronto — Hands-On Lab")

st.write("")

st.markdown("#### Welcome, eh!")

st.markdown("""
From coast to coast to coast, data lives everywhere — in object storage, open table formats, and cloud catalogs.
This hands-on lab shows you how Snowflake meets your data where it is, without moving a single byte.
""")

st.write("")

st.markdown("#### How this workshop works")

st.markdown("""
This guide provides **step-by-step SQL instructions** for each session. You'll work entirely in **Snowsight** — Snowflake's web interface:

- **SQL blocks** — copy each block into a Snowsight worksheet and run it
- **Snowsight UI walkthroughs** — follow guided steps to test agents and explore CoWork
- **Natural language exploration** — ask questions in plain English against your lakehouse data

All sections build on each other sequentially — work through them in order.
""")

st.write("")

st.markdown("#### The scenario")
with st.container(border=True):
    st.markdown("""
Connect to Apache Iceberg tables in AWS S3 via Catalog-Linked Databases with **zero data movement**.
Register an existing AWS Glue catalog in seconds, making external tables instantly discoverable and queryable.

Apply **Snowflake Horizon** governance — RBAC and dynamic masking policies — to your Iceberg tables.
Then leverage **Snowflake CoWork** to ask natural language questions against your lakehouse
with AI-generated verifiable SQL at enterprise scale.

**The dataset:** Insurance quote requests stored as Apache Iceberg in AWS S3, registered in the
AWS Glue Data Catalog. ~56,000 records with customer, policy, and pricing attributes — a common
pattern in Canadian insurance analytics for identifying churn risk and high quote frequency.
""")

st.write("")

st.markdown("#### What you'll build")

with st.container(border=True):
    st.markdown("""
**1. Connect to the Lakehouse** — Create an External Volume, Catalog Integration, and Catalog-Linked Database
that auto-discovers Iceberg tables from AWS Glue. No data copies, no ETL.

**2. Query Iceberg Data** — Run SQL against Iceberg tables as if they were native Snowflake tables.
Explore insurance quote volumes, product breakdowns, and premium distributions by credit score.

**3. Govern Your Lakehouse** — Apply Snowflake Horizon governance to external Iceberg data. Create roles
with different access levels and dynamic data masking policies that protect PII — all without
moving data into Snowflake.

**4. Define Business Semantics** — Create a Semantic View that defines metrics, dimensions, and facts
on your Iceberg data, enabling AI to understand and query your lakehouse in natural language.

**5. Ask Questions in Plain English** — Build a Cortex Agent and use Snowflake CoWork to query your
data lake conversationally. Masking policies are enforced end-to-end from Iceberg through the
agent response.
""")

st.write("")

st.markdown("#### Prerequisites")
with st.container(border=True):
    st.markdown("""
- Snowflake Enterprise account with **ACCOUNTADMIN** role — see **Getting Started** for free trial setup
- Account deployed in **AWS US East 2 (Ohio)** — the lab infrastructure is in this region
- A modern web browser for Snowsight
""")

st.write(""); st.write("")
st.caption("Power Analytics and AI Wherever Your Data Lives — Snowflake World Tour Toronto")
