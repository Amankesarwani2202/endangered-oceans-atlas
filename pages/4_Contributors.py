import sys
from pathlib import Path
import time
import streamlit as st
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from community import GitHubStore, StorageError, ROLES, month_now, read_content, make_submission
from data import COMMON_CSS

from navigation import render_sidebar

st.set_page_config(page_title="Contributors · Oceans Atlas", page_icon="💬", layout="wide")

render_sidebar()
st.markdown(COMMON_CSS, unsafe_allow_html=True)
st.title("💬 Ocean voices")
st.write("Science educators, professors, students and researchers: share your perspective on our monthly question.")
questions = read_content("questions.json")
current = month_now()
question = questions.get(current)
try:
    config = dict(st.secrets.get("community", {}))
except FileNotFoundError:
    config = {}
try:
    store = GitHubStore(config)
except StorageError as exc:
    store = None
    st.info(str(exc))
if question:
    st.subheader(f"Question of the month · {current}")
    st.write(question)
    with st.form("contribute"):
        name = st.text_input("Display name", max_chars=100)
        role = st.selectbox("Your role (self-reported)", ROLES)
        institution = st.text_input("Institution / organisation (optional, public)", max_chars=150)
        answer = st.text_area("Your answer", max_chars=5000, height=180)
        consent = st.checkbox("I agree to publish my display name, role, institution and answer on this website and in its newsletter. I have permission to share this content.")
        st.caption("Do not include private contact details or sensitive information. Answers are reviewed before publication. Roles are not verified.")
        submitted = st.form_submit_button("Submit for review", disabled=store is None)
    if submitted:
        try:
            if time.time() - st.session_state.get("last_submission", 0) < 60:
                raise ValueError("Please wait one minute before submitting another answer.")
            if month_now() != current:
                raise ValueError("The month has changed. Refresh to answer the new question.")
            record = make_submission(current, question, name, role, institution, answer, consent)
            key = (current, name.strip(), role, institution.strip(), answer.strip())
            if st.session_state.get("submission_key") == key:
                record = st.session_state["submission_record"]
            else:
                st.session_state.submission_key = key
                st.session_state.submission_record = record
            store.save(record)
            st.session_state.last_submission = time.time()
            st.success("Your answer has been saved for editorial review. Thank you!")
        except (ValueError, StorageError) as exc:
            st.error(str(exc))
else:
    st.info("The next monthly question will be announced soon. Browse previous contributions below.")
st.divider()
st.subheader("Community feed")
month = st.selectbox("Browse month", sorted(set(questions) | {current}, reverse=True))
if month in questions:
    st.write(questions[month])
if store:
    try:
        records = [r for r in store.records(month) if r.get("status") == "approved" and r.get("consent")]
        if not records:
            st.info("No published answers for this month yet.")
        for record in records:
            with st.container(border=True):
                st.text(record["name"])
                st.caption(" · ".join(filter(None, [record["role"], record.get("institution"), record["submitted_at"][:10]])))
                st.text(record["answer"])
    except StorageError as exc:
        st.error(str(exc))
