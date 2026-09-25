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
    5,
    "Natural Language Queries",
    "15 min",
    "Cortex Agent and Agent Studio for conversational analytics on your data lake",
)

render_technologies_used([
    {
        "name": "Cortex Agent",
        "description": "An AI assistant backed by your semantic view. Translates plain English into SQL against your Iceberg data, with masking enforced end-to-end.",
        "icon": "smart_toy",
    },
    {
        "name": "Agent Studio",
        "description": "The Snowsight interface for creating, reviewing, and testing Cortex Agents. Preview tab provides a chat interface; 'Preview in Snowflake CoWork' opens the full collaborative experience.",
        "icon": "tune",
    },
    {
        "name": "End-to-End Governance",
        "description": "Masking policies flow from Iceberg through the view, semantic view, and agent. Role-based access is enforced at every layer.",
        "icon": "verified_user",
    },
])

st.markdown("---")

st.markdown("""
A Cortex Agent wraps the semantic view and exposes it as a **natural language interface**.
Snowflake translates plain English questions into SQL against your Iceberg data -- masking
policies are enforced automatically based on the querying role.
""")

st.write("")

render_coco_prompt(
    "5.1",
    "Create Cortex Agent",
    "Create a new worksheet for the Cortex Agent. "
    "Create a Cortex Agent called quotes_agent in iceberg_lab_db.analytics with display name "
    "'Canadian Insurance Quotes Analyst'. It should use a cortex_analyst_text_to_sql tool called "
    "'Query Insurance Quotes' backed by the quotes_sv semantic view.\n\n"
    "Agent instructions: Answer questions about insurance quote data. Use the quotes tool to query "
    "premium amounts, product types, homeowner status, marital status, and postcode district. "
    "Summarize results clearly with a Canadian perspective -- reference provinces and regional patterns "
    "where relevant. Format currency values in CAD. Suggest follow-up questions to deepen analysis.",
    sql="""\
USE ROLE ACCOUNTADMIN;
USE DATABASE iceberg_lab_db;
USE SCHEMA analytics;

CREATE OR REPLACE AGENT iceberg_lab_db.analytics.quotes_agent
  WITH PROFILE = '{"display_name": "Canadian Insurance Quotes Analyst"}'
  COMMENT = 'Natural language analytics on Iceberg insurance quotes data in AWS Glue'
FROM SPECIFICATION $$
{
  "instructions": {
    "response": "Answer questions about insurance quote data. Use the quotes tool to query premium amounts, product types, homeowner status, marital status, and postcode district. Summarize results clearly with a Canadian perspective -- reference provinces and regional patterns where relevant. Format currency values in CAD. Suggest follow-up questions to deepen analysis."
  },
  "tools": [
    {
      "tool_spec": {
        "type": "cortex_analyst_text_to_sql",
        "name": "Query Insurance Quotes",
        "description": "Query insurance quote data including premiums, product types, homeowner status, marital status, and postcode district."
      }
    }
  ],
  "tool_resources": {
    "Query Insurance Quotes": {
      "semantic_view": "iceberg_lab_db.analytics.quotes_sv"
    }
  }
}
$$;""",
    note="The agent uses the semantic view to translate natural language into SQL.",
)

render_explanation("How the agent works", """
The Cortex Agent is a first-class Snowflake object that:

1. **Receives** a plain English question from the user
2. **Translates** it into SQL using the semantic view definitions (facts, dimensions, metrics)
3. **Executes** the SQL against `quotes_vw` -- which reads from the Iceberg table via the CLD
4. **Returns** the result with natural language explanation

**Governance flows end-to-end:**
- The agent queries `quotes_sv` which resolves to `quotes_vw`
- `quotes_vw` has masking policies applied
- If the user's role is `lab_analyst`, PII columns are automatically masked in the agent's response
- If the user's role is `lab_data_engineer`, full values are visible

The agent instructions include a **Canadian perspective** -- referencing provinces, regional patterns,
and CAD currency formatting.
""")

st.write("")

st.markdown("---")

st.markdown("#### :material/smart_toy: 5.2 -- Test Your Agent in Agent Studio")

with st.container(border=True):
    st.markdown("""
Open your agent in Agent Studio to review its configuration and test it with natural language questions.

1. In the Snowsight left navigation panel, select **AI & ML** and then **Agent Studio**
2. Find **Canadian Insurance Quotes Analyst** in the list and click to open it
3. Optionally, review the agent specification that CoCo generated in the previous step -- you can see the tool configuration, semantic view binding, and agent instructions
4. Click the **Preview** tab to open the chat interface
5. Type a question and press Enter -- the agent translates it into SQL against your Iceberg data

You can test the agent directly in the Preview tab, or click **Preview in Snowflake CoWork** for the full collaborative experience.
    """)

st.write("")

st.markdown("##### Sample questions")
st.markdown("Try these questions to explore the agent:")

questions = [
    ("Product breakdown", "How many quotes are there by product type?"),
    ("Homeowner comparison", "What is the average premium for homeowners vs non-homeowners?"),
    ("Regional analysis", "Which postal districts have the highest average risk premium?"),
    ("Multi-dimension", "Show me quote volume broken down by marital status and product type."),
    ("Credit score insight", "Compare average premiums across credit score bands."),
    ("Previous insurer", "What is the total premium volume by previous insurer?"),
]

for label, question in questions:
    with st.container(border=True):
        st.markdown(f"**{label}**")
        st.code(question, language="text", wrap_lines=True)

st.write("")

st.markdown("##### Test masking enforcement")
with st.container(border=True):
    st.markdown("""
Switch between roles to see how masking affects agent responses:

1. In Snowsight, use the **role picker** (top-left) to switch to `lab_analyst`
2. Ask: *"Show me the customers with the highest total premium"*
3. Notice that `surname`, `email`, `phonenumber`, and `dateofbirth` are **masked**
4. Switch to `lab_data_engineer` and ask the same question
5. Now you see **full PII values**

The same Iceberg data, the same agent, the same question -- governance controls who sees what,
all the way from S3 through the AI response.
""")

st.markdown("---")

render_key_concepts([
    {
        "term": "Cortex Agent",
        "definition": "A first-class Snowflake object that orchestrates LLMs and tools to answer complex questions. Uses the semantic view to translate natural language into SQL. Created via CREATE AGENT SQL or the Snowsight UI.",
    },
    {
        "term": "Text-to-SQL Tool",
        "definition": "The cortex_analyst_text_to_sql tool type connects the agent to a semantic view. The agent generates SQL from natural language using the semantic view's facts, dimensions, and metrics definitions.",
    },
    {
        "term": "Agent Studio",
        "definition": "The Snowsight interface for creating, reviewing, and testing Cortex Agents. The Preview tab provides a chat interface for testing agents directly. 'Preview in Snowflake CoWork' opens the full collaborative experience.",
    },
    {
        "term": "End-to-End Governance",
        "definition": "Masking policies applied to the view wrapper flow through the semantic view and agent response. The same question produces different results depending on the querying role -- no additional configuration needed.",
    },
])

render_what_you_built([
    "quotes_agent -- Cortex Agent with Canadian Insurance Quotes Analyst persona",
    "Natural language analytics on Iceberg data via semantic view",
    "Tested the agent in Agent Studio and verified end-to-end masking enforcement",
    "Analysts see masked PII, data engineers see full values -- governed from Iceberg to AI response",
])

st.markdown("---")

st.markdown("#### Congratulations!")

st.markdown("""
You've built a complete open lakehouse analytics stack:

1. **Connected** Snowflake to AWS Glue via a Catalog-Linked Database
2. **Queried** Iceberg tables with zero data movement
3. **Governed** external data with Snowflake Horizon -- RBAC and dynamic masking
4. **Defined** business semantics for AI-ready analytics
5. **Built** a Cortex Agent for natural language queries with end-to-end governance

The same Iceberg data in AWS Glue, governed and queried entirely by Snowflake -- from coast to coast.
""")

st.write("")

st.markdown("##### Related resources")

st.markdown("""
- [Apache Iceberg tables in Snowflake](https://docs.snowflake.com/en/user-guide/tables-iceberg)
- [Catalog-Linked Databases](https://docs.snowflake.com/en/user-guide/tables-iceberg-catalog-linked-database)
- [Configure a catalog integration for AWS Glue Iceberg REST](https://docs.snowflake.com/en/user-guide/tables-iceberg-configure-catalog-integration-rest-glue)
- [Dynamic Data Masking](https://docs.snowflake.com/en/user-guide/security-column-ddm-intro)
- [Semantic Views](https://docs.snowflake.com/en/user-guide/views-semantic)
- [Cortex Agents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agent)
""")
