import streamlit as st

st.title("Agenda")
st.markdown("Five sessions building a complete open lakehouse analytics stack on Snowflake.")

st.write("")

st.markdown("#### Session overview")

sessions = [
    ("1", "Create Snowflake Objects", "5 min", "External Volume, Catalog Integration, Catalog-Linked Database"),
    ("2", "Query Iceberg Data", "10 min", "SQL queries against Iceberg tables in AWS Glue -- zero data movement"),
    ("3", "Data Governance", "15 min", "Roles, dynamic data masking policies on Iceberg data via Snowflake Horizon"),
    ("4", "Semantic View", "15 min", "Business metrics and dimensions for AI-ready analytics"),
    ("5", "Natural Language Queries", "15 min", "Cortex Agent and Agent Studio for conversational analytics"),
]

for num, title, duration, description in sessions:
    with st.container(border=True):
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"### Session {num}")
            st.caption(duration)
        with col2:
            st.markdown(f"**{title}**")
            st.caption(description)

st.write("")

st.markdown("#### What you'll build")

st.markdown("""
| Object | Type | Purpose |
|--------|------|---------|
| `my_iceberg_vol` | External Volume | S3 storage access for Iceberg data files |
| `my_glue_int` | Catalog Integration | Connection to AWS Glue Iceberg REST endpoint |
| `my_iceberg_db` | Catalog-Linked Database | Auto-discovers and syncs tables from Glue |
| `lab_data_engineer` | Role | Full access to PII columns |
| `lab_analyst` | Role | Masked access to PII columns |
| `quotes_vw` | View | Wrapper for masking policy attachment |
| 4 masking policies | Masking Policy | Protect email, phone, surname, date of birth |
| `quotes_sv` | Semantic View | Business metrics and dimensions on Iceberg data |
| `quotes_agent` | Cortex Agent | Natural language analytics on your data lake |
""")

st.write("")

col1, col2 = st.columns(2)
col1.metric("Total duration", "~60 min")
col2.metric("Sessions", "5")

st.write("")
st.caption("Power Analytics and AI Wherever Your Data Lives — Snowflake World Tour Canada")
