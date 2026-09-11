import streamlit as st

st.title("Getting Started")
st.markdown("Set up your Snowflake trial account for the lab.")

st.write("")

st.markdown("#### Step 1: Sign up for a Snowflake trial")
with st.container(border=True):
    col1, col2, col3 = st.columns(3)
    col1.metric("Trial duration", "30 days")
    col2.metric("Free credits", "$400")
    col3.metric("Credit card", "Not required")

    st.markdown("""
1. Go to [signup.snowflake.com](https://signup.snowflake.com/?t=612344c843109dd7e4235d855aa00cb626979d51b072e87b10b3813d4ae0ff12&cloud=aws&region=us-east-2)

> **Important:** You must use the link above — do not type the address manually.
> This link provisions a trial account with **Cortex AI capabilities enabled** and
> pre-selects **AWS US East 2 (Ohio)**, which is required because the lab infrastructure
> (S3 bucket, Glue catalog, IAM role) is deployed in this region.
""")

st.write("")

st.markdown("#### Step 2: Activate your account")
with st.container(border=True):
    st.markdown("""
1. Check your email for the activation link
2. Click the link and set your password
3. Log in to [app.snowflake.com](https://app.snowflake.com/)
""")

st.write("")

st.markdown("#### Step 3: Open a Snowsight worksheet")
with st.container(border=True):
    st.markdown("""
Session 1 uses direct SQL in a **Snowsight worksheet**:

1. Log in to [app.snowflake.com](https://app.snowflake.com/)
2. Click **Projects** in the left nav, then **Worksheets**
3. Click **+** (top right) to create a new SQL worksheet
4. Set your role to **ACCOUNTADMIN** using the role picker in the top-left corner
5. Set your warehouse to **COMPUTE_WH** (or the warehouse available in your account)

**How to run SQL blocks from this guide:**
- **Run all statements:** Press `Ctrl + Shift + Enter` (Windows/Linux) or `Cmd + Shift + Return` (Mac)
- **Run a single statement:** Place your cursor inside it and press `Ctrl + Enter` or `Cmd + Return`
""")

st.write("")

st.markdown("#### Step 4: Open CoCo in Snowsight")
with st.container(border=True):
    st.markdown("""
Sessions 2-5 use **CoCo** (Cortex Code) — Snowflake's AI coding assistant built into Snowsight.
You'll paste natural language prompts into CoCo and it will generate and run the SQL for you.

**To open CoCo:**
1. In Snowsight, look for the **CoCo chat panel** — it's available in worksheets and throughout the UI
2. You can also access it via the **AI & ML** section in the left sidebar

**How it works:**
- Each step in Sessions 2-5 gives you a **CoCo prompt** to copy and paste
- CoCo generates the SQL, explains what it's doing, and runs it in your account
- The collapsible **SQL** section under each prompt shows what CoCo will produce
""")

st.write("")

st.markdown("#### You're ready!")
with st.container(border=True):
    st.markdown("""
Once you can see the Snowsight worksheet editor with **ACCOUNTADMIN** role selected,
you're ready to start **Session 1: Create Snowflake Objects**.

No additional software, CLI tools, or AWS credentials are needed — the AWS infrastructure
has been pre-configured for you.
""")
