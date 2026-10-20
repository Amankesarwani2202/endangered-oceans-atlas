"""One shared top navigation menu with explicit, consistent page icons."""
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


def render_navigation():
    st.markdown("""
    <style>
    .st-key-atlas-top-navigation {
        border: 1px solid rgba(75,133,157,.2); border-radius: 14px;
        padding: 1rem 1.15rem; margin-bottom: 1.2rem;
        background: var(--secondary-background-color);
    }
    .st-key-atlas-top-navigation [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap; gap: .25rem .5rem;
    }
    .st-key-atlas-top-navigation [data-testid="stColumn"] {
        flex: 1 0 auto !important; width: auto !important; min-width: fit-content !important;
    }
    .st-key-atlas-top-navigation [data-testid="stPageLink"] a {
        padding: .55rem .7rem; border-radius: 9px; min-height: 2.6rem;
    }
    .st-key-atlas-top-navigation [data-testid="stPageLink"] a:hover {
        background: rgba(18,107,128,.08);
    }
    .st-key-atlas-top-navigation [data-testid="stPageLink"] a[aria-current="page"] {
        background: rgba(18,107,128,.14); font-weight: 600;
        box-shadow: inset 0 -2px #126b80;
    }
    @media (max-width:640px) {
        .st-key-atlas-top-navigation { padding: .8rem; }
    }
    </style>
    """, unsafe_allow_html=True)
    with st.container(key="atlas-top-navigation"):
        st.markdown("**🌊 Oceans Atlas**")
        links = [link for _, group in GROUPS for link in group]
        for col, (path, label, icon) in zip(st.columns(len(links), gap="small"), links):
            with col:
                st.page_link(path, label=label, icon=icon, use_container_width=True)
