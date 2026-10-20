import sys
from pathlib import Path
import streamlit as st
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from community import read_content, safe_url
from data import COMMON_CSS
st.set_page_config(page_title="Newsletters · Oceans Atlas", page_icon="📰", layout="wide")
st.markdown(COMMON_CSS, unsafe_allow_html=True)
st.title("📰 Ocean voices newsletter")
st.write("Monthly perspectives from our contributors, collected and designed by our editorial team in Canva.")
issues = sorted(read_content("newsletters.json"), key=lambda n: n["month"], reverse=True)
if not issues:
    st.info("Our first newsletter is on its way. Visit Contributors to answer this month's question.")
for issue in issues:
    with st.container(border=True):
        st.subheader(issue["title"])
        st.caption(issue["month"])
        st.write(issue.get("description", ""))
        if safe_url(issue.get("url", "")):
            st.link_button("Read newsletter ↗", issue["url"])
        if issue.get("pdf"):
            folder = Path(__file__).resolve().parents[1] / "content/newsletters"
            path = (folder / issue["pdf"]).resolve()
            if path.is_relative_to(folder.resolve()) and path.suffix.lower() == ".pdf" and path.is_file():
                st.download_button("Download PDF", path.read_bytes(), file_name=path.name, mime="application/pdf", key=issue["month"])
