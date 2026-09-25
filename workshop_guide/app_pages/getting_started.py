import streamlit as st
from pathlib import Path

_STATIC = Path(__file__).parent.parent / "static"

st.title("Getting Started")
st.markdown("Claim your lab account and log in to Snowflake.")

st.write("")

st.markdown("#### Claim your account")
with st.container(border=True):
    st.markdown(
        "Click the following link to claim your account for the hands-on lab: "
        "[go.dataops.live/swt-toronto-iceberg-hol/register](https://go.dataops.live/swt-toronto-iceberg-hol/register)"
    )

st.write("")

st.markdown("#### Step 1: Register")
with st.container(border=True):
    st.markdown(
        "Enter your **email address** and click **Register**."
    )
    st.image(str(_STATIC / "hol_signup.png"), caption="Enter your email address and click Register")

st.write("")

st.markdown("#### Step 2: Check your email")
with st.container(border=True):
    st.markdown(
        "Check your email for your **account info**, then click **Sign in** with your info."
    )
    st.image(str(_STATIC / "hol_signup2.png"), caption="Check your email for account info, then sign in")

st.write("")

st.markdown("#### Step 3: Open Snowflake")
with st.container(border=True):
    st.markdown(
        "When you see the section for **event instructions**, click the **URL** to open Snowflake."
    )
    st.image(str(_STATIC / "hol_signup3.png"), caption="Click the URL in the event instructions to open Snowflake")

st.write("")

st.markdown("#### Step 4: Log in to Snowflake")
with st.container(border=True):
    st.markdown(
        "Log in to Snowflake using the identified **username** and **password**:"
    )
    st.markdown("- **Username:** `USER`\n- **Password:** `sn0wf@ll`")

st.write("")

st.markdown("#### Step 5: Set up multi-factor authentication")
with st.container(border=True):
    st.markdown(
        "You will be asked to create a **multi-factor authentication** method. "
        "Choose one of the methods available. We suggest **passkey** as the most straightforward option."
    )

st.write("")

st.markdown("#### You're ready!")
with st.container(border=True):
    st.markdown(
        "Once logged in you will be presented with the Snowflake home screen and you are ready to start the hands-on lab!"
    )
    st.image(str(_STATIC / "snowflake_home.png"), caption="Snowflake Home screen -- you're ready to begin")

    st.markdown("""
No additional software, CLI tools, or AWS credentials are needed -- the AWS infrastructure
has been pre-configured for you. Head to **Session 1: Create Snowflake Objects** to begin.
""")
