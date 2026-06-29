import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data import load_data, COMMON_CSS

st.set_page_config(page_title="Analysis · Endangered Oceans Atlas", page_icon="📊", layout="wide")
st.markdown(COMMON_CSS, unsafe_allow_html=True)

marine_species = load_data()

st.markdown('<div class="page-title">📊 Threat Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Visual breakdown of the crisis across species, oceans, and threat types.</div>', unsafe_allow_html=True)

# ── Charts row 1 ─────────────────────────────────────────────
c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown("#### Status Distribution")
    status_counts = marine_species.status.value_counts()
    color_map = {
        "Critically Endangered": "#c0392b",
        "Endangered": "#e67e22",
        "Vulnerable": "#27ae60",
    }
    try:
        import plotly.express as px
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            color=status_counts.index,
            color_discrete_map=color_map,
            hole=0.45,
        )
        fig.update_layout(
            showlegend=True, margin=dict(t=10, b=10, l=10, r=10),
            font_family="Inter",
        )
        st.plotly_chart(fig, use_container_width=True)
    except ImportError:
        st.bar_chart(status_counts)

with c2:
    st.markdown("#### Species by Ocean Region")
    ocean_counts = marine_species.ocean.value_counts()
    try:
        fig2 = px.bar(
            x=ocean_counts.values,
            y=ocean_counts.index,
            orientation="h",
            color=ocean_counts.values,
            color_continuous_scale=["#a8d4f0","#0a3d62"],
            labels={"x": "Number of Species", "y": ""},
        )
        fig2.update_layout(
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(t=10, b=10, l=10, r=10),
            font_family="Inter",
        )
        st.plotly_chart(fig2, use_container_width=True)
    except ImportError:
        st.bar_chart(ocean_counts)

# ── Charts row 2 ─────────────────────────────────────────────
st.markdown("---")
c3, c4 = st.columns(2, gap="large")

with c3:
    st.markdown("#### Threat Categories")
    # Extract simplified threat keywords
    threat_keywords = {
        "Overfishing / Bycatch": ["overfishing","bycatch","fishing","gillnet"],
        "Climate Change": ["climate","warming","bleaching","ice"],
        "Illegal Trade": ["illegal trade","finning","poaching","fin trade"],
        "Habitat Loss": ["habitat","reef","seagrass"],
        "Ship Strikes": ["ship","strikes","entanglement"],
        "Hunting": ["hunting","whaling"],
    }
    threat_counts = {}
    for threat, keywords in threat_keywords.items():
        count = marine_species.primary_threat.str.lower().apply(
            lambda t: any(k in t for k in keywords)
        ).sum()
        if count:
            threat_counts[threat] = int(count)
    threat_series = pd.Series(threat_counts).sort_values(ascending=True)

    try:
        fig3 = px.bar(
            x=threat_series.values,
            y=threat_series.index,
            orientation="h",
            color=threat_series.values,
            color_continuous_scale=["#f5b7b1","#c0392b"],
            labels={"x":"Species Affected","y":""},
        )
        fig3.update_layout(
            showlegend=False, coloraxis_showscale=False,
            margin=dict(t=10,b=10,l=10,r=10), font_family="Inter",
        )
        st.plotly_chart(fig3, use_container_width=True)
    except ImportError:
        st.bar_chart(threat_series)

with c4:
    st.markdown("#### Status × Ocean Region Heatmap")
    pivot = marine_species.groupby(["ocean","status"]).size().unstack(fill_value=0)
    try:
        import plotly.graph_objects as go
        fig4 = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns.tolist(),
            y=pivot.index.tolist(),
            colorscale=[[0,"#f0f8ff"],[0.5,"#1a6fa5"],[1,"#0a3d62"]],
            showscale=True,
            text=pivot.values,
            texttemplate="%{text}",
        ))
        fig4.update_layout(
            margin=dict(t=10,b=10,l=10,r=10), font_family="Inter",
            xaxis_title="", yaxis_title="",
        )
        st.plotly_chart(fig4, use_container_width=True)
    except ImportError:
        st.dataframe(pivot)

# ── Key insights ─────────────────────────────────────────────
st.markdown("---")
st.markdown("#### Key Insights")

insights = [
    ("🔴", "6 of 15 tracked species are **Critically Endangered** — that's 40% of our dataset."),
    ("🌊", "The **Indian Ocean** and **Bay of Bengal** host the most at-risk species in this dataset."),
    ("🎣", "**Overfishing and bycatch** are the single most pervasive threat, affecting 9 of 15 species."),
    ("🌡️", "**Climate change** is an emerging multiplier threat, compounding risks for coral, turtles, and whales."),
    ("🦈", "Sharks are heavily over-represented — 4 of 15 species are sharks, all facing extinction-level pressure."),
]

cols = st.columns(1)
for icon, text in insights:
    st.markdown(
        f'<div style="background:#f0f8ff;border-left:4px solid #1a6fa5;border-radius:0 10px 10px 0;'
        f'padding:.75rem 1rem;margin-bottom:.6rem;font-size:.9rem;color:#1a3a5c">'
        f'{icon} {text}</div>',
        unsafe_allow_html=True,
    )

# ── Full data table ───────────────────────────────────────────
st.markdown("---")
with st.expander("📄 View Full Dataset"):
    display = marine_species[["emoji","species_name","status","ocean","population_estimate","primary_threat","conservation_action"]].copy()
    display.columns = ["","Species","Status","Ocean","Population","Threat","Conservation"]
    st.dataframe(display.reset_index(drop=True), use_container_width=True, hide_index=True)
    