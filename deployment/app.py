"""NovaBank Support Console - deployable Streamlit app.

Minimal runnable shell so `uv run streamlit run deployment/app.py` works from a
fresh clone and the three-column layout is verifiable before any agent exists.

Wiring to the core agent happens at T-064; every panel below is a placeholder.

Plan: PROJECT_PLAN.md sections 13 and 14
Tasks: T-064 (chat), T-065 (context rail), T-066 (citations), T-067 (activity)
Status: SKELETON - layout only, no agent connected.
"""

from __future__ import annotations

import streamlit as st

st.set_page_config(
    page_title="NovaBank Support Console",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- synthetic-data banner: permanent, non-dismissible -----------------------
st.warning(
    "**SYNTHETIC DEMO DATA** - NovaBank is fictional. No real bank, customer, "
    "policy or financial advice is represented.",
    icon="⚠️",
)

st.title("🏦 NovaBank Support Console")
st.caption("Life-Event Financial Navigator - non-transactional advisory agent")

# --- session state ----------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "demo-thread-1"

# --- left rail: customer context (T-065) ------------------------------------
with st.sidebar:
    st.subheader("Customer context")
    st.info("Mock context loads via read-only MCP tools at T-065.")
    st.metric("Customer", "C-1042")
    st.metric("Segment", "Retail")

    st.divider()
    st.subheader("Detected life event")
    st.write("_none yet_")

    st.divider()
    if st.button("Reset session", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- main split: conversation | agent activity ------------------------------
chat_col, activity_col = st.columns([2, 1], gap="large")

with chat_col:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask about a life event..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # TODO(T-064): replace with core_agent.respond(prompt, session)
        placeholder = (
            "_Agent not wired up yet._ This shell exists so the layout and "
            "session handling are verifiable from Milestone 0."
        )
        st.session_state.messages.append({"role": "assistant", "content": placeholder})
        with st.chat_message("assistant"):
            st.markdown(placeholder)

    st.subheader("Sources")
    st.caption("Policy citations render here, one expander per retrieved document.")

with activity_col:
    st.subheader("Agent activity")
    st.caption("Gates, tool calls and retrieval populate from trace data at T-067.")
    for step in [
        "Gate 0 (input)",
        "Life-event detection",
        "Risk assessment",
        "Tool calls",
        "Policy retrieval",
        "Gate 2 (evidence)",
        "Gate 3 (output)",
    ]:
        st.write(f"- {step} - _pending_")
