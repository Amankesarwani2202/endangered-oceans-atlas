import streamlit as st
import folium
from folium.plugins import MarkerCluster, HeatMap, Fullscreen
from streamlit_folium import st_folium

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data import load_data, STATUS_COLORS, STATUS_ICONS, STATUS_HEX_BG, STATUS_HEX_FG, COMMON_CSS

st.set_page_config(page_title="Map · Endangered Oceans Atlas", page_icon="🗺️", layout="wide")
st.markdown(COMMON_CSS, unsafe_allow_html=True)

marine_species = load_data()

# ── Sidebar filters ───────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔍 Filter Species")
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
    st.markdown("---")
    st.markdown("### 🗺️ Map Layers")
    show_clusters = st.checkbox("Species Markers", value=True)
    show_heatmap  = st.checkbox("Biodiversity Heatmap", value=True)
    st.markdown("---")
    map_tile = st.selectbox("Base Map", ["CartoDB positron", "OpenStreetMap", "CartoDB dark_matter"])
    st.caption("Data is illustrative. Sources: IUCN Red List, WWF, NOAA.")

filtered = marine_species[
    marine_species.status.isin(selected_statuses) &
    marine_species.ocean.isin(selected_oceans)
]

# ── Header ────────────────────────────────────────────────────
st.markdown('<div class="page-title">🗺️ Interactive Map</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Click any marker for species details, threats, and conservation actions.</div>', unsafe_allow_html=True)

# Stat pills
c1, c2, c3, c4 = st.columns(4)
for col, num, label, color in [
    (c1, len(filtered), "Shown", "#0a3d62"),
    (c2, len(filtered[filtered.status == "Critically Endangered"]), "Critically Endangered", "#c0392b"),
    (c3, len(filtered[filtered.status == "Endangered"]), "Endangered", "#e67e22"),
    (c4, len(filtered[filtered.status == "Vulnerable"]), "Vulnerable", "#1a6b3a"),
]:
    col.markdown(
        f'<div style="background:{color};color:white;border-radius:10px;padding:.7rem;text-align:center;">'
        f'<div style="font-size:1.8rem;font-weight:700">{num}</div>'
        f'<div style="font-size:.7rem;opacity:.85;text-transform:uppercase;letter-spacing:.08em">{label}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── Build map ─────────────────────────────────────────────────
ocean_map = folium.Map(location=[20, 0], zoom_start=2, tiles=map_tile)

if show_heatmap and not filtered.empty:
    HeatMap(
        filtered[["latitude", "longitude"]].values.tolist(),
        name="Biodiversity Heatmap",
        radius=40, blur=30,
        gradient={"0.2": "#1a6fa5", "0.5": "#f39c12", "1.0": "#c0392b"},
    ).add_to(ocean_map)

if show_clusters and not filtered.empty:
    mc = MarkerCluster(name="Species Markers").add_to(ocean_map)
    for _, row in filtered.iterrows():
        bg = STATUS_HEX_BG.get(row.status, "#fff3cd")
        fg = STATUS_HEX_FG.get(row.status, "#856404")
        popup_html = f"""
        <div style="width:280px;font-family:'Segoe UI',sans-serif;padding:4px;">
            <h3 style="color:#0a3d62;margin:0 0 6px 0;">{row.emoji} {row.species_name}</h3>
            <hr style="margin:4px 0;border-color:#cce0f5;">
            <p style="margin:4px 0;"><b>Status:</b>
                <span style="background:{bg};color:{fg};padding:1px 8px;border-radius:999px;font-size:.8em;font-weight:600;">{row.status}</span></p>
            <p style="margin:4px 0;"><b>Ocean:</b> {row.ocean}</p>
            <p style="margin:4px 0;"><b>Population:</b> {row.population_estimate}</p>
            <p style="margin:4px 0;"><b>Primary Threat:</b> {row.primary_threat}</p>
            <p style="margin:4px 0;"><b>Conservation:</b> {row.conservation_action}</p>
            <hr style="margin:6px 0;border-color:#cce0f5;">
            <p style="margin:2px 0;color:#0a3d62;font-weight:600;font-size:.85em;">💡 Fun Fact</p>
            <p style="margin:2px 0;font-size:.82em;color:#444;font-style:italic;">{row.fun_fact}</p>
            <hr style="margin:6px 0;border-color:#cce0f5;">
            <p style="margin:2px 0;color:#0a3d62;font-weight:600;font-size:.85em;">🤝 How You Can Help</p>
            <p style="margin:2px 0;font-size:.82em;color:#333;">{row.how_you_can_help}</p>
        </div>"""
        folium.Marker(
            location=[row.latitude, row.longitude],
            popup=folium.Popup(popup_html, max_width=340),
            tooltip=f"{row.emoji} {row.species_name} — {row.status}",
            icon=folium.Icon(
                color=STATUS_COLORS.get(row.status, "blue"),
                icon=STATUS_ICONS.get(row.status, "info-sign"),
            ),
        ).add_to(mc)

Fullscreen(position="topleft", title="Full Screen", title_cancel="Exit Full Screen", force_separate_button=True).add_to(ocean_map)
folium.LayerControl(collapsed=False).add_to(ocean_map)

# ── Layout ────────────────────────────────────────────────────
map_col, table_col = st.columns([3, 2], gap="medium")

with map_col:
    st_folium(ocean_map, width="100%", height=520, returned_objects=[])

with table_col:
    st.markdown("#### Species in View")
    if filtered.empty:
        st.info("No species match the current filters.")
    else:
        for _, row in filtered.iterrows():
            bg = STATUS_HEX_BG.get(row.status, "#fff3cd")
            fg = STATUS_HEX_FG.get(row.status, "#856404")
            with st.expander(f"{row.emoji}  {row.species_name}"):
                st.markdown(
                    f'<span style="background:{bg};color:{fg};padding:2px 10px;border-radius:999px;font-size:.75rem;font-weight:600">'
                    f'{row.status}</span>&nbsp;<small style="color:#666">{row.ocean}</small>',
                    unsafe_allow_html=True,
                )
                st.markdown(f"**Population:** {row.population_estimate}")
                st.markdown(f"**Threat:** {row.primary_threat}")
                st.markdown(f"**Conservation:** {row.conservation_action}")
                st.info(f"🤝 {row.how_you_can_help}")

# ── Legend ────────────────────────────────────────────────────
st.markdown("---")
l1, l2, l3, _ = st.columns([1, 1, 1, 3])
l1.markdown("🔴 **Critically Endangered**")
l2.markdown("🟠 **Endangered**")
l3.markdown("🟢 **Vulnerable**")
st.caption("Built with Streamlit · folium · streamlit-folium | Data: IUCN Red List, WWF, NOAA")