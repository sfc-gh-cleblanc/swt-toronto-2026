# Power Analytics and AI Wherever Your Data Lives

## Snowflake World Tour Canada — Hands-On Lab

### Overview

Connect to Apache Iceberg tables in AWS S3 via Catalog-Linked Databases with zero data movement.
Register existing AWS Glue catalogs in seconds, making external tables instantly discoverable
and queryable. Apply Snowflake Horizon governance including RBAC and dynamic masking policies
to your Iceberg tables. Then leverage Snowflake CoWork to ask natural language questions against
your lakehouse with AI-generated verifiable SQL at enterprise scale.

### Duration

~75 minutes (5 sessions)

### Platform

- Snowflake Enterprise account (AWS US West 2 — Oregon)
- ACCOUNTADMIN access required
- Warehouse: COMPUTE_WH

### Pre-Configured AWS Infrastructure

| Component | Value |
|-----------|-------|
| S3 Bucket | `s3://sf-lab-iceberg-407539788379/iceberg/` |
| Glue Database | `iceberg` |
| Iceberg Table | `quotes` (~56K insurance quote records) |
| IAM Role | `arn:aws:iam::407539788379:role/sf-lab-shared-role` |

### Sessions

| # | Session | Duration | What You Build |
|---|---------|----------|----------------|
| 1 | Create Snowflake Objects | 15 min | External Volume, Catalog Integration, Catalog-Linked Database |
| 2 | Query Iceberg Data | 10 min | SQL queries on Iceberg tables — zero data movement |
| 3 | Data Governance | 20 min | Roles, dynamic masking policies via Snowflake Horizon |
| 4 | Semantic View | 15 min | Business metrics and dimensions for AI analytics |
| 5 | Natural Language Queries | 15 min | Cortex Agent + Snowflake CoWork |

### Snowflake Objects Created

| Object | Type |
|--------|------|
| `my_iceberg_vol` | External Volume |
| `my_glue_int` | Catalog Integration |
| `my_iceberg_db` | Catalog-Linked Database |
| `iceberg_lab_db` | Database (governance + analytics) |
| `lab_data_engineer` | Role |
| `lab_analyst` | Role |
| `quotes_vw` | View (masking wrapper) |
| `mask_email`, `mask_phone`, `mask_surname`, `mask_dob` | Masking Policies |
| `quotes_sv` | Semantic View |
| `quotes_agent` | Cortex Agent |

### Technologies Covered

- Apache Iceberg (V2 format)
- AWS Glue Iceberg REST Catalog (IRC)
- External Volumes and Catalog Integrations
- Catalog-Linked Databases
- Snowflake Horizon (RBAC + Dynamic Data Masking)
- Semantic Views
- Cortex Agents
- Snowflake CoWork

### How to Run

The workshop guide is a Streamlit app. To run locally:

```bash
cd workshop_guide
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Or use GitHub Codespaces — the devcontainer is pre-configured.
