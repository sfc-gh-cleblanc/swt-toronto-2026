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
    3,
    "Data Governance",
    "15 min",
    "Roles, dynamic data masking, and Snowflake Horizon governance on Iceberg data",
)

render_technologies_used([
    {
        "name": "Snowflake Horizon",
        "description": "Snowflake's governance framework. Applies natively to Iceberg tables in a CLD  --  data never needs to move for policies to take effect.",
        "icon": "shield",
    },
    {
        "name": "Dynamic Data Masking",
        "description": "Column-level policies that mask PII based on the querying role. Analysts see redacted values; engineers see full data.",
        "icon": "visibility_off",
    },
    {
        "name": "Role-Based Access Control",
        "description": "Snowflake RBAC with a role hierarchy  --  lab_analyst is a subset of lab_data_engineer, controlling who sees what.",
        "icon": "admin_panel_settings",
    },
])

st.markdown("---")

st.markdown("""
Snowflake Horizon governance policies apply **natively** to Iceberg tables in a Catalog-Linked
Database. The data never needs to move into Snowflake storage for policies to take effect.

In this session you'll create two roles with different access levels, then apply dynamic
data masking to PII columns. Analysts see partially masked data; data engineers see full values.
""")

st.write("")

render_coco_prompt(
    "3.1",
    "Create Roles",
    "Create a new worksheet for data governance. "
    "Create two roles: lab_data_engineer and lab_analyst. "
    "Set up a hierarchy where lab_analyst is a subset of lab_data_engineer. "
    "Grant both roles to my current user and give them USAGE on COMPUTE_WH.",
    sql="""\
USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS lab_data_engineer;
CREATE ROLE IF NOT EXISTS lab_analyst;

-- Hierarchy: analyst is a subset of data engineer
GRANT ROLE lab_analyst TO ROLE lab_data_engineer;

-- Grant both roles to your user
GRANT ROLE lab_data_engineer TO USER IDENTIFIER(CURRENT_USER());
GRANT ROLE lab_analyst TO USER IDENTIFIER(CURRENT_USER());

-- Grant warehouse access so roles can run queries
GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE lab_data_engineer;
GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE lab_analyst;""",
    note="Creates a role hierarchy where lab_analyst is a subset of lab_data_engineer.",
)

render_explanation("Role hierarchy design", """
The role hierarchy follows a **principle of least privilege**:

- **lab_analyst**  --  can query data but sees masked PII
- **lab_data_engineer**  --  inherits analyst access plus sees full PII values
- **ACCOUNTADMIN**  --  owns everything, sees all data

Because `lab_analyst` is granted TO `lab_data_engineer`, the engineer role automatically
inherits all analyst privileges. This is standard RBAC design in Canadian enterprise
environments where privacy regulations (PIPEDA, provincial privacy acts) require
clear data access tiers.
""")

st.write("")

render_coco_prompt(
    "3.2",
    "Grant Access to Lakehouse Objects",
    "Grant both lab_data_engineer and lab_analyst access to query the Iceberg data. "
    "They need USAGE on my_iceberg_vol, my_glue_int, the my_iceberg_db database and its \"iceberg\" schema, "
    "and SELECT on all Iceberg tables in that schema.",
    sql="""\
-- External volume and catalog integration
GRANT USAGE ON EXTERNAL VOLUME my_iceberg_vol TO ROLE lab_data_engineer;
GRANT USAGE ON INTEGRATION my_glue_int TO ROLE lab_data_engineer;

-- Catalog-linked database
GRANT USAGE ON DATABASE my_iceberg_db TO ROLE lab_data_engineer;
GRANT USAGE ON DATABASE my_iceberg_db TO ROLE lab_analyst;
GRANT USAGE ON SCHEMA my_iceberg_db."iceberg" TO ROLE lab_data_engineer;
GRANT USAGE ON SCHEMA my_iceberg_db."iceberg" TO ROLE lab_analyst;
GRANT SELECT ON ALL ICEBERG TABLES IN SCHEMA my_iceberg_db."iceberg" TO ROLE lab_data_engineer;
GRANT SELECT ON ALL ICEBERG TABLES IN SCHEMA my_iceberg_db."iceberg" TO ROLE lab_analyst;""",
)

render_explanation("Why grant access to both roles?", """
Both roles need access to the Iceberg table so they can query it. The **masking policies**
(created next) control *what data they see*, not *whether they can query*.

Note the use of `GRANT SELECT ON ALL ICEBERG TABLES`  --  this grants access to all current
tables in the Glue-synced schema. New tables discovered by future syncs will need
additional grants.
""")

st.write("")

render_coco_prompt(
    "3.3",
    "Create View Wrapper",
    "Create a database called iceberg_lab_db with a schema called analytics. "
    "Then create a view called quotes_vw in that schema that selects all 40 columns from my_iceberg_db.\"iceberg\".\"quotes\", "
    "aliasing every lowercase Glue column name to its uppercase equivalent  --  for example \\\"uuid\\\" AS UUID, \\\"quote_product\\\" AS QUOTE_PRODUCT. "
    "This normalises the lowercase Iceberg/Glue identifiers to standard Snowflake uppercase so that masking policies and the Semantic View work correctly. "
    "Do not use SELECT *  --  explicitly alias all 40 columns.",
    sql="""\
CREATE DATABASE IF NOT EXISTS iceberg_lab_db;
CREATE SCHEMA IF NOT EXISTS iceberg_lab_db.analytics;

CREATE OR REPLACE VIEW iceberg_lab_db.analytics.quotes_vw AS
SELECT
    "uuid"                AS UUID,
    "quote_product"       AS QUOTE_PRODUCT,
    "quotedate"           AS QUOTEDATE,
    "policyno"            AS POLICYNO,
    "creditscore"         AS CREDITSCORE,
    "newriskpremium"      AS NEWRISKPREMIUM,
    "surname"             AS SURNAME,
    "email"               AS EMAIL,
    "phonenumber"         AS PHONENUMBER,
    "dateofbirth"         AS DATEOFBIRTH,
    "postcodedistrict"    AS POSTCODEDISTRICT,
    "maritalstatus"       AS MARITALSTATUS,
    "homeownerind"        AS HOMEOWNERIND,
    "sex"                 AS SEX,
    "previnsr"            AS PREVINSR,
    "vehiclemake"         AS VEHICLEMAKE,
    "vehiclemodel"        AS VEHICLEMODEL,
    "vehicleage"          AS VEHICLEAGE,
    "driverage"           AS DRIVERAGE,
    "ncd_years"           AS NCD_YEARS,
    "voluntary_excess"    AS VOLUNTARY_EXCESS,
    "compulsory_excess"   AS COMPULSORY_EXCESS,
    "cover_type"          AS COVER_TYPE,
    "payment_frequency"   AS PAYMENT_FREQUENCY,
    "annual_mileage"      AS ANNUAL_MILEAGE,
    "occupation"          AS OCCUPATION,
    "licence_type"        AS LICENCE_TYPE,
    "licence_years"       AS LICENCE_YEARS,
    "claims_count"        AS CLAIMS_COUNT,
    "convictions_count"   AS CONVICTIONS_COUNT,
    "address_line1"       AS ADDRESS_LINE1,
    "city"                AS CITY,
    "county"              AS COUNTY,
    "country"             AS COUNTRY,
    "quote_channel"       AS QUOTE_CHANNEL,
    "quote_status"        AS QUOTE_STATUS,
    "renewal_flag"        AS RENEWAL_FLAG,
    "totalpremiumpayable" AS TOTALPREMIUMPAYABLE,
    "iptamount"           AS IPTAMOUNT,
    "quote_record"        AS QUOTE_RECORD
FROM my_iceberg_db."iceberg"."quotes";""",
    note="Aliasing to uppercase here means all downstream objects  --  masking policies, semantic view, and Cortex Agent  --  use standard Snowflake identifiers without double quotes.",
)

render_explanation("Why a view wrapper?", """
Masking policies in Snowflake are attached to **columns on views or tables**. Tables in a
Catalog-Linked Database are externally managed, so policies cannot be applied to them directly.

The solution: create a **view wrapper** (`quotes_vw`) that selects all columns from the
Iceberg table. But there is a second reason to use a view: AWS Glue stores all column names in
**lowercase** (e.g. `uuid`, `homeownerind`, `totalpremiumpayable`). Snowflake treats unquoted
identifiers as uppercase, so referencing these columns without double quotes fails.

By aliasing every column to uppercase in the view (`"uuid" AS UUID`, `"homeownerind" AS HOMEOWNERIND`),
all downstream objects  --  masking policies, the Semantic View, and the Cortex Agent  --  can reference
columns using standard unquoted Snowflake identifiers. This is the correct pattern whenever building
on top of external catalog data (AWS Glue, Unity Catalog, Polaris) that uses lowercase column names.
""")

st.write("")

render_coco_prompt(
    "3.4",
    "Create Masking Policies",
    "In iceberg_lab_db.analytics, create four dynamic masking policies:\n"
    "1. mask_email  --  shows first character + ***@***.domain for non-privileged roles\n"
    "2. mask_phone  --  shows first 3 and last 3 digits with asterisks in between\n"
    "3. mask_surname  --  shows first character + asterisks\n"
    "4. mask_dob  --  shows ****-**- plus the last 2 digits (day)\n\n"
    "LAB_DATA_ENGINEER and ACCOUNTADMIN should see the real values. All other roles see masked data.",
    sql="""\
USE DATABASE iceberg_lab_db;
USE SCHEMA analytics;

-- Email masking: first character + ***@***.domain
CREATE OR REPLACE MASKING POLICY mask_email
  AS (val STRING) RETURNS STRING ->
    CASE
      WHEN CURRENT_ROLE() IN ('LAB_DATA_ENGINEER', 'ACCOUNTADMIN') THEN val
      ELSE CONCAT(LEFT(val, 1), '***@***.', SPLIT_PART(val, '.', -1))
    END;

-- Phone masking: first 3 + asterisks + last 3 digits
CREATE OR REPLACE MASKING POLICY mask_phone
  AS (val STRING) RETURNS STRING ->
    CASE
      WHEN CURRENT_ROLE() IN ('LAB_DATA_ENGINEER', 'ACCOUNTADMIN') THEN val
      ELSE CONCAT(LEFT(val, 3), REPEAT('*', LENGTH(val) - 6), RIGHT(val, 3))
    END;

-- Surname masking: first character + asterisks
CREATE OR REPLACE MASKING POLICY mask_surname
  AS (val STRING) RETURNS STRING ->
    CASE
      WHEN CURRENT_ROLE() IN ('LAB_DATA_ENGINEER', 'ACCOUNTADMIN') THEN val
      ELSE CONCAT(LEFT(val, 1), REPEAT('*', GREATEST(LENGTH(val) - 1, 4)))
    END;

-- Date of birth masking: ****-**-DD (day only visible)
CREATE OR REPLACE MASKING POLICY mask_dob
  AS (val STRING) RETURNS STRING ->
    CASE
      WHEN CURRENT_ROLE() IN ('LAB_DATA_ENGINEER', 'ACCOUNTADMIN') THEN val
      ELSE CONCAT('****-**-', RIGHT(val, 2))
    END;""",
    note="Each policy checks CURRENT_ROLE()  --  engineers and admins see real values, everyone else sees masked data.",
)

render_explanation("How dynamic masking works", """
Each masking policy is a **SQL function** that takes a column value and returns either the
real value or a masked version, based on the querying role.

The four PII columns protected:
| Column | Masking pattern | Example |
|--------|----------------|---------|
| `email` | First char + `***@***.` + domain | `j***@***.com` |
| `phonenumber` | First 3 + asterisks + last 3 | `XXX*****XXX` |
| `surname` | First char + asterisks | `S****` |
| `dateofbirth` | `****-**-` + day | `****-**-15` |

This approach is compliant with Canadian privacy regulations (PIPEDA) which require that
personal information be protected but allow authorized roles to access it for legitimate
business purposes.
""")

st.write("")

render_coco_prompt(
    "3.5",
    "Apply Masking Policies to View",
    "Apply the four masking policies to the corresponding columns on iceberg_lab_db.analytics.quotes_vw:\n"
    "- mask_email on the email column\n"
    "- mask_phone on the phonenumber column\n"
    "- mask_surname on the surname column\n"
    "- mask_dob on the dateofbirth column\n\n"
    "Use ALTER VIEW ... ALTER COLUMN ... SET MASKING POLICY for each.",
    sql="""\
USE ROLE ACCOUNTADMIN;

ALTER VIEW iceberg_lab_db.analytics.quotes_vw
  ALTER COLUMN email SET MASKING POLICY iceberg_lab_db.analytics.mask_email;

ALTER VIEW iceberg_lab_db.analytics.quotes_vw
  ALTER COLUMN phonenumber SET MASKING POLICY iceberg_lab_db.analytics.mask_phone;

ALTER VIEW iceberg_lab_db.analytics.quotes_vw
  ALTER COLUMN surname SET MASKING POLICY iceberg_lab_db.analytics.mask_surname;

ALTER VIEW iceberg_lab_db.analytics.quotes_vw
  ALTER COLUMN dateofbirth SET MASKING POLICY iceberg_lab_db.analytics.mask_dob;""",
    note="Masking is enforced whenever the view is queried  --  in SQL, via the semantic view, or through the agent.",
)

st.write("")

render_coco_prompt(
    "3.6",
    "Verify Masking",
    "Verify the masking policies work by querying iceberg_lab_db.analytics.quotes_vw as two different roles. "
    "First switch to lab_analyst and select uuid, surname, email, phonenumber, dateofbirth, totalpremiumpayable (limit 5). "
    "Then switch to lab_data_engineer and run the same query. Show me the difference.",
    sql="""\
-- As analyst: PII is masked
USE ROLE lab_analyst;
SELECT uuid, surname, email, phonenumber, dateofbirth, totalpremiumpayable
FROM iceberg_lab_db.analytics.quotes_vw
LIMIT 5;

-- As data engineer: full values visible
USE ROLE lab_data_engineer;
SELECT uuid, surname, email, phonenumber, dateofbirth, totalpremiumpayable
FROM iceberg_lab_db.analytics.quotes_vw
LIMIT 5;""",
    note="Run both queries and compare  --  the same Iceberg data, governed entirely by Snowflake.",
)

render_explanation("End-to-end governance on external data", """
What makes this powerful:

1. The data **never moved**  --  it's still Iceberg on S3, managed by AWS Glue
2. Snowflake governance (RBAC + masking) applies **at query time**
3. The same policies will flow through to the **Semantic View** and **Cortex Agent** in later sessions
4. No AWS-side policy changes were needed

This is the same Iceberg data in AWS Glue, governed entirely by Snowflake  --  zero data
movement, zero copies, zero AWS-side policy changes needed.
""")

st.markdown("---")

render_key_concepts([
    {
        "term": "Dynamic Data Masking",
        "definition": "A column-level security feature that applies masking functions at query time based on the querying role. The underlying data is never modified  --  masking is applied on read.",
    },
    {
        "term": "View Wrapper Pattern",
        "definition": "A thin view over an external table that enables governance features (masking, row access policies) that cannot be applied directly to CLD tables. The view is also the target for semantic views.",
    },
    {
        "term": "PIPEDA Compliance",
        "definition": "Canada's Personal Information Protection and Electronic Documents Act. Requires organizations to protect personal information and limit access to authorized purposes. Dynamic masking helps enforce this at the data layer.",
    },
])

render_what_you_built([
    "lab_data_engineer and lab_analyst roles with proper hierarchy",
    "Grants on External Volume, Catalog Integration, and CLD objects",
    "quotes_vw  --  view wrapper for governance policy attachment",
    "4 masking policies protecting email, phone, surname, and date of birth",
    "Verified role-based masking on the same Iceberg data",
])
