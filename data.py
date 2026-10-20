import pandas as pd
import streamlit as st

STATUS_COLORS    = {"Critically Endangered": "red", "Endangered": "orange", "Vulnerable": "green"}
STATUS_TAG_CLASS = {"Critically Endangered": "tag-cr", "Endangered": "tag-en", "Vulnerable": "tag-vu"}
STATUS_ICONS     = {"Critically Endangered": "exclamation-sign", "Endangered": "warning-sign", "Vulnerable": "info-sign"}
STATUS_HEX_BG    = {"Critically Endangered": "#ffe0e0", "Endangered": "#fff3cd", "Vulnerable": "#e2f0e8"}
STATUS_HEX_FG    = {"Critically Endangered": "#c0392b", "Endangered": "#856404", "Vulnerable": "#1a6b3a"}

COMMON_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@300;400;500;600&display=swap');
html, body, [class*="css"] { font-family: "Inter", sans-serif; }
.tag { display:inline-block; padding:2px 10px; border-radius:999px; font-size:.72rem; font-weight:600; }
.tag-cr { background:#ffe0e0; color:#c0392b; }
.tag-en { background:#fff3cd; color:#856404; }
.tag-vu { background:#e2f0e8; color:#1a6b3a; }
.page-title { font-family:"Playfair Display",serif; font-size:2rem; font-weight:900; color:#0a3d62; margin-bottom:.2rem; }
.page-sub   { color:#4a6fa5; font-size:.95rem; font-weight:300; margin-bottom:1.4rem; }
div[data-testid="stSidebar"] { background:#f5f9ff; }
</style>
"""


@st.cache_data
def load_data() -> pd.DataFrame:
    from pathlib import Path
    import json
    records = json.loads((Path(__file__).parent / "content/species.json").read_text())
    return pd.DataFrame(records)
