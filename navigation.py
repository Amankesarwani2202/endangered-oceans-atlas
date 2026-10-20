"""One shared sidebar menu with explicit, consistent page icons."""
import streamlit as st

GROUPS = [
    ("Explore", [("Home.py", "Home", "🏠"),
                 ("pages/1_🗺️_Map.py", "Map", "🗺️"),
                 ("pages/2_📋_Species.py", "Species", "🐋"),
                 ("pages/3_📊_Analysis.py", "Analysis", "📊")]),
    ("Community", [("pages/4_Contributors.py", "Contributors", "💬"),
                   ("pages/5_Newsletters.py", "Newsletters", "📰")]),
    ("Manage", [("pages/6_Editor.py", "Editor", "🔐")]),
]


def render_sidebar():
    with st.sidebar:
        st.markdown("### 🌊 Oceans Atlas")
        st.caption("Explore marine life. Share ideas. Protect our oceans.")
        for title, links in GROUPS:
            st.caption(title.upper())
            for path, label, icon in links:
                st.page_link(path, label=label, icon=icon, use_container_width=True)
        st.divider()
