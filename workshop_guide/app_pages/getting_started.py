import streamlit as st
from pathlib import Path

_STATIC = Path(__file__).parent.parent / "static"

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
2. Enter your **name**, **email**, **company**, and **title**, then click **Sign Up**

> **Important:** You must use the link above -- do not type the address manually.
> This link provisions a trial account with **Cortex AI capabilities enabled** and
> pre-selects **AWS US East 2 (Ohio)**, which is required because the lab infrastructure
> (S3 bucket, Glue catalog, IAM role) is deployed in this region.
""")

st.write("")

st.markdown("#### Step 2: Activate your account and log in")
with st.container(border=True):
    st.markdown("""
1. Check your email for a message from **Snowflake Computing** with the subject "Activate your Snowflake account"
2. Click the **CLICK TO ACTIVATE** link in the email. This will open a web browser prompting you to set a username and password for your trial account. Enter your preferred username and choose a password to log in.
""")
    st.image(str(_STATIC / "activation_email.png"), caption="Activation email from Snowflake")

    st.markdown("""
Once logged in you will be presented with the Snowflake Home screen and you are ready to start the hands-on lab!
""")
    st.image(str(_STATIC / "snowflake_home.png"), caption="Snowflake Home screen -- you're ready to begin")

st.write("")

st.markdown("#### You're ready!")
with st.container(border=True):
    st.markdown("""
Once you can see the Snowflake Home screen you're ready to start **Session 1: Create Snowflake Objects**.

No additional software, CLI tools, or AWS credentials are needed -- the AWS infrastructure
has been pre-configured for you.
""")
