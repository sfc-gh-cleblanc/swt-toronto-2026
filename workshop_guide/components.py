import streamlit as st

SESSION_PROMPTS = {
    1: ["1.1", "1.2", "1.3", "1.4"],
    2: ["2.1", "2.2", "2.3", "2.4"],
    3: ["3.1", "3.2", "3.3", "3.4", "3.5", "3.6"],
    4: ["4.1", "4.2", "4.3"],
    5: ["5.1", "5.2"],
}


def _done_store() -> dict:
    if "_done" not in st.session_state:
        st.session_state["_done"] = {}
    return st.session_state["_done"]


def _prompt_key(prompt_id: str) -> str:
    return prompt_id.replace(" ", "_").replace(".", "_")


def _on_toggle(prompt_id: str):
    key = _prompt_key(prompt_id)
    _done_store()[key] = st.session_state[f"_cb_{key}"]


def is_session_complete(session_num: int) -> bool:
    prompts = SESSION_PROMPTS.get(session_num, [])
    store = _done_store()
    return len(prompts) > 0 and all(
        store.get(_prompt_key(p), False) for p in prompts
    )


def render_sql_block(block_id: str, title: str, sql: str, note: str = ""):
    key = _prompt_key(block_id)
    cb_key = f"_cb_{key}"
    store = _done_store()
    if cb_key not in st.session_state:
        st.session_state[cb_key] = store.get(key, False)
    with st.container(border=True):
        header_col, check_col = st.columns([5, 1])
        with header_col:
            st.markdown(f"#### :material/code: {block_id} — {title}")
        with check_col:
            st.checkbox("Done", key=cb_key, on_change=_on_toggle, args=(block_id,))
        st.caption("Copy this SQL and run it in your Snowsight worksheet")
        st.code(sql, language="sql", wrap_lines=True)
        if note:
            st.caption(note)


def render_coco_prompt(block_id: str, title: str, prompt_text: str, sql: str = "", note: str = ""):
    key = _prompt_key(block_id)
    cb_key = f"_cb_{key}"
    store = _done_store()
    if cb_key not in st.session_state:
        st.session_state[cb_key] = store.get(key, False)
    with st.container(border=True):
        header_col, check_col = st.columns([5, 1])
        with header_col:
            st.markdown(f"#### :material/terminal: {block_id} — {title}")
        with check_col:
            st.checkbox("Done", key=cb_key, on_change=_on_toggle, args=(block_id,))
        st.caption("Copy this prompt and paste it into CoCo")
        st.code(prompt_text, language="text", wrap_lines=True)
        if note:
            st.caption(note)
        if sql:
            with st.expander(":material/code: SQL that CoCo will generate", expanded=False):
                st.code(sql, language="sql", wrap_lines=True)
        st.markdown(
            "Place your cursor on each SQL statement in the worksheet and press "
            "`Ctrl + Enter` (Windows/Linux) or `Cmd + Return` (Mac) to run it interactively and see the results."
        )


def render_explanation(title: str, body: str):
    with st.expander(f":material/school: {title}", expanded=False):
        st.markdown(body)


def render_technology_card(name: str, description: str, icon: str = "widgets"):
    with st.container(border=True):
        st.markdown(f":material/{icon}: **{name}**")
        st.caption(description)


def render_technologies_used(technologies: list[dict]):
    st.markdown("##### :material/build: Technologies used in this session")
    cols = st.columns(min(len(technologies), 3))
    for i, tech in enumerate(technologies):
        with cols[i % len(cols)]:
            render_technology_card(
                tech["name"], tech["description"], tech.get("icon", "widgets")
            )


def render_session_header(
    session_num: int,
    title: str,
    duration: str,
    building: str,
):
    st.title(f"Session {session_num}: {title}")
    col1, col2 = st.columns(2)
    col1.markdown(f":material/schedule: **{duration}**")
    col2.markdown(f":material/construction: **Building**: {building}")
    st.write("")


def render_key_concepts(concepts: list[dict]):
    st.markdown("##### :material/lightbulb: Key concepts")
    for concept in concepts:
        with st.expander(f"**{concept['term']}**"):
            st.markdown(concept["definition"])


def render_what_you_built(items: list[str]):
    st.markdown("##### :material/check_circle: What you built in this session")
    for item in items:
        st.markdown(f"- :green-badge[Done] {item}")
