from pathlib import Path

import streamlit as st

from components import is_session_complete

_DIR = Path(__file__).parent


def _title(session_num: int, label: str) -> str:
    check = " :green[:material/check_circle:]" if is_session_complete(session_num) else ""
    return f"{session_num}. {label}{check}"


st.set_page_config(
    page_title="Power Analytics & AI — Wherever Your Data Lives",
    page_icon=":material/public:",
    layout="wide",
)

st.logo(
    str(_DIR / "static" / "snowflake_full_logo.png"),
    icon_image=str(_DIR / "static" / "snowflake_logo.png"),
)

page = st.navigation(
    {
        "": [
            st.Page("app_pages/home.py", title="Home", icon=":material/home:"),
            st.Page("app_pages/getting_started.py", title="Getting Started", icon=":material/rocket_launch:"),
            st.Page("app_pages/agenda.py", title="Agenda", icon=":material/calendar_today:"),
        ],
        "Workshop Sessions": [
            st.Page("app_pages/session_01.py", title=_title(1, "Create Snowflake Objects"), icon=":material/link:"),
            st.Page("app_pages/session_02.py", title=_title(2, "Query Iceberg Data"), icon=":material/query_stats:"),
            st.Page("app_pages/session_03.py", title=_title(3, "Data Governance"), icon=":material/shield:"),
            st.Page("app_pages/session_04.py", title=_title(4, "Semantic View"), icon=":material/schema:"),
            st.Page("app_pages/session_05.py", title=_title(5, "Natural Language Queries"), icon=":material/chat:"),
        ],
    },
    position="sidebar",
)

page.run()
