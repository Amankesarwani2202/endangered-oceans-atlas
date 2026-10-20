import sys
from pathlib import Path
import hmac
import time
import streamlit as st
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data import COMMON_CSS
from community import GitHubStore, StorageError, month_now, read_content, export_answers
from navigation import render_navigation

st.set_page_config(page_title="Editor · Oceans Atlas", page_icon="🔐", layout="wide")

render_navigation()
st.markdown(COMMON_CSS, unsafe_allow_html=True)
st.title("🔐 Editorial desk")
try:
    config = dict(st.secrets.get("community", {}))
except FileNotFoundError:
    config = {}
password = config.get("editor_password", "")
if not password:
    st.info("The editorial desk has not been configured.")
    st.stop()
if not st.session_state.get("editor_authenticated"):
    with st.form("editor_login"):
        entered = st.text_input("Editor password", type="password")
        login = st.form_submit_button("Sign in")
    if login:
        if time.time() < st.session_state.get("login_after", 0):
            st.error("Please wait before trying again.")
        elif hmac.compare_digest(entered.encode(), password.encode()):
            st.session_state.editor_authenticated = True
            st.session_state.editor_expires = time.time() + 3600
            st.rerun()
        else:
            st.session_state.login_after = time.time() + 5
            st.error("Incorrect password.")
    st.stop()
if time.time() > st.session_state.get("editor_expires", 0) or st.button("Sign out"):
    st.session_state.editor_authenticated = False
    st.rerun()
st.caption("Review submissions before publication. Access expires after one hour. Roles and affiliations are self-reported.")
section = st.radio("Editor section", ["Contributions", "Manage species"], horizontal=True)
if section == "Manage species":
    from species_editor import render_species_editor
    render_species_editor(config)
    st.stop()
month = st.selectbox("Submission month", sorted(set(read_content("questions.json")) | {month_now()}, reverse=True))
try:
    store = GitHubStore(config)
    records = store.records(month)
    st.download_button("Export ALL submissions for editorial review (CSV)", export_answers(records), file_name=f"ocean-voices-{month}-all.csv", mime="text/csv")
    approved = [r for r in records if r["status"] == "approved" and r.get("consent")]
    st.download_button("Export approved answers for Canva (CSV)", export_answers(approved), file_name=f"ocean-voices-{month}-approved.csv", mime="text/csv")
    st.caption("The all-submissions export includes pending and rejected answers. Use the approved export for publication. Canva design and publication are manual; see COMMUNITY_SETUP.md.")
    state = st.selectbox("Filter status", ["pending", "approved", "rejected", "all"])
    visible = [r for r in records if state == "all" or r["status"] == state]
    if not visible:
        st.info("No answers in this view.")
    for record in visible:
        with st.container(border=True):
            st.text(f"{record['name']} · {record['role']} · {record['status']}")
            st.text(record.get("institution", ""))
            st.caption(record["submitted_at"])
            st.write(record["question"])
            st.text(record["answer"])
            choice = st.selectbox("Publication status", ["pending", "approved", "rejected"], index=["pending", "approved", "rejected"].index(record["status"]), key=record["id"])
            if st.button("Save decision", key="save_" + record["id"]):
                record["status"] = choice
                store.save(record)
                st.rerun()
except StorageError as exc:
    st.error(str(exc))
