import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data import load_data, STATUS_HEX_BG, STATUS_HEX_FG, COMMON_CSS

st.set_page_config(page_title="Species · Endangered Oceans Atlas", page_icon="📋", layout="wide")
st.markdown(COMMON_CSS, unsafe_allow_html=True)

st.markdown("""
<style>
.species-hero {
    background: linear-gradient(135deg,#0a3d62,#1a6fa5);
    border-radius:16px; padding:2rem 2.4rem; color:white; margin-bottom:1.8rem;
}
.species-hero h1 { font-family:"Playfair Display",serif; font-size:2rem; font-weight:900; margin:0 0 .4rem; }
.species-hero p  { font-size:.95rem; font-weight:300; opacity:.85; margin:0; }
.sp-card {
    background:#ffffff; border:1px solid #d0e4f5; border-radius:16px;
    padding:1.4rem; margin-bottom:1rem;
    transition:box-shadow .2s;
}
.sp-card:hover { box-shadow:0 6px 20px rgba(10,61,98,.1); }
.sp-name { font-size:1.05rem; font-weight:600; color:#0a3d62; }
.sp-ocean { font-size:.8rem; color:#5a7fa0; }
.sp-pop   { font-size:.82rem; color:#333; margin-top:.25rem; }
.sp-threat { font-size:.82rem; color:#c0392b; }
.sp-help   { background:#f0f8ff; border-radius:8px; padding:.65rem .9rem; font-size:.84rem; color:#0a3d62; margin-top:.6rem; }
.sp-fact   { background:#fffbf0; border-radius:8px; padding:.65rem .9rem; font-size:.84rem; color:#7d5800; margin-top:.4rem; font-style:italic; }
</style>
""", unsafe_allow_html=True)

marine_species = load_data()

# ── Sidebar filters ───────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔍 Filter")
    selected_statuses = st.multiselect(
        "Threat Status",
        sorted(marine_species.status.unique()),
        default=sorted(marine_species.status.unique()),
    )
    selected_oceans = st.multiselect(
        "Ocean / Region",
        sorted(marine_species.ocean.unique()),
        default=sorted(marine_species.ocean.unique()),
    )
    search = st.text_input("Search species name", placeholder="e.g. Whale")
    st.markdown("---")
    view_mode = st.radio("View", ["Cards", "Table"], horizontal=True)

filtered = marine_species[
    marine_species.status.isin(selected_statuses) &
    marine_species.ocean.isin(selected_oceans)
]
if search:
    filtered = filtered[filtered.species_name.str.contains(search, case=False)]

# ── Header ────────────────────────────────────────────────────
st.markdown("""
<div class="species-hero">
  <h1>📋 Species Directory</h1>
  <p>Detailed profiles of all 15 tracked marine species — their populations, threats, and what you can do.</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"**{len(filtered)} species** match your filters.")

# ── Content ───────────────────────────────────────────────────
if view_mode == "Table":
    display_cols = ["emoji","species_name","status","ocean","population_estimate","primary_threat"]
    rename_map   = {"emoji":"","species_name":"Species","status":"Status","ocean":"Ocean",
                    "population_estimate":"Population","primary_threat":"Primary Threat"}
    st.dataframe(
        filtered[display_cols].rename(columns=rename_map).reset_index(drop=True),
        use_container_width=True, hide_index=True,
    )
else:
    # Card grid: 2 columns
    cols = st.columns(2, gap="medium")
    for i, (_, row) in enumerate(filtered.iterrows()):
        bg = STATUS_HEX_BG.get(row.status, "#fff3cd")
        fg = STATUS_HEX_FG.get(row.status, "#856404")
        with cols[i % 2]:
            st.markdown(f"""
            <div class="sp-card">
              <div style="display:flex;align-items:center;gap:.7rem;margin-bottom:.5rem;">
                <span style="font-size:2rem;">{row.emoji}</span>
                <div>
                  <div class="sp-name">{row.species_name}</div>
                  <div class="sp-ocean">{row.ocean}</div>
                </div>
                <span style="margin-left:auto;background:{bg};color:{fg};padding:2px 10px;
                             border-radius:999px;font-size:.72rem;font-weight:600;white-space:nowrap;">
                  {row.status}
                </span>
              </div>
              <div class="sp-pop">👥 <b>Population:</b> {row.population_estimate}</div>
              <div class="sp-threat">⚠️ <b>Threat:</b> {row.primary_threat}</div>
              <div class="sp-threat" style="color:#1a6fa5;">🛡️ <b>Conservation:</b> {row.conservation_action}</div>
              <div class="sp-help">🤝 {row.how_you_can_help}</div>
              <div class="sp-fact">💡 {row.fun_fact}</div>
            </div>
            """, unsafe_allow_html=True)

if filtered.empty:
    st.info("No species match your current filters. Try broadening your search.")