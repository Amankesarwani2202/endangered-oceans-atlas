# ============================================================
# 🌊 Endangered Oceans Atlas — Google Colab Single Cell
# ============================================================
# Just run this cell. A public URL will appear at the bottom.
# ============================================================

# ── 1. Install dependencies ──────────────────────────────────
!pip install -q streamlit folium streamlit-folium pandas pyngrok

# ── 2. Write the Streamlit app to a file ─────────────────────
app_code = '''
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap, Fullscreen
from streamlit_folium import st_folium

st.set_page_config(page_title="🌊 Endangered Oceans Atlas", page_icon="🌊", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Sans+3:wght@300;400;600&display=swap');
    html, body, [class*="css"] { font-family: "Source Sans 3", sans-serif; }
    .main-title { font-family: "Playfair Display", serif; font-size: 2.4rem; color: #0a3d62; }
    .subtitle   { color: #4a6fa5; font-size: 1rem; font-weight: 300; margin-bottom: 1.2rem; }
    .stat-card  {
        background: linear-gradient(135deg, #0a3d62, #1a6fa5);
        border-radius: 12px; padding: 1rem; color: white; text-align: center;
        box-shadow: 0 4px 15px rgba(10,61,98,0.2);
    }
    .stat-number { font-size: 2rem; font-weight: 700; }
    .stat-label  { font-size: 0.75rem; opacity: 0.85; text-transform: uppercase; letter-spacing: 0.08em; }
    .species-card {
        background: #f0f7ff; border-left: 4px solid #1a6fa5;
        border-radius: 0 10px 10px 0; padding: 0.8rem 1rem; margin-bottom: 0.6rem;
    }
    .tag { display:inline-block; padding:2px 10px; border-radius:999px; font-size:0.72rem; font-weight:600; }
    .tag-cr { background:#ffe0e0; color:#c0392b; }
    .tag-en { background:#fff3cd; color:#856404; }
    .tag-vu { background:#e2f0e8; color:#1a6b3a; }
    div[data-testid="stSidebar"] { background: #f5f9ff; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.DataFrame({
        "species_name": [
            "Blue Whale","Hawksbill Turtle","Vaquita","Dugong","Whale Shark",
            "Great Hammerhead Shark","Leatherback Turtle","Narwhal",
            "Irrawaddy Dolphin","Oceanic Whitetip Shark","Sei Whale",
            "Green Turtle","Humphead Wrasse","Shortfin Mako Shark","Staghorn Coral",
        ],
        "latitude":  [-33.86,15.87,31.50,18.50,12.00,-5.00,10.00,75.00,20.00,15.00,-40.00,20.00,-5.00,30.00,-18.00],
        "longitude": [151.20,73.82,-114.00,72.80,88.30,55.00,-60.00,-80.00,95.00,-30.00,20.00,80.00,145.00,-40.00,148.00],
        "status": [
            "Endangered","Critically Endangered","Critically Endangered","Vulnerable","Endangered",
            "Critically Endangered","Vulnerable","Vulnerable","Endangered","Critically Endangered",
            "Endangered","Endangered","Endangered","Endangered","Critically Endangered",
        ],
        "ocean": [
            "Pacific Ocean","Indian Ocean","Gulf of California","Indian Ocean","Bay of Bengal",
            "Indian Ocean","Atlantic Ocean","Arctic Ocean","Bay of Bengal","Atlantic Ocean",
            "Southern Ocean","Indian Ocean","Pacific Ocean","Atlantic Ocean","Pacific Ocean",
        ],
        "population_estimate": [
            "10,000–25,000","~8,000","<10","~100,000","~180,000",
            "<1,000","~34,000–36,000","~123,000","~7,000","<1,000",
            "~50,000–80,000","~100,000","~1,000","~3,000,000 (declining)","<1% of 1980s levels",
        ],
        "primary_threat": [
            "Ship strikes, entanglement","Illegal trade, habitat loss","Gillnet bycatch",
            "Habitat loss, hunting","Fishing bycatch, fin trade","Overfishing, bycatch",
            "Entanglement, climate change","Climate change, hunting","Bycatch, habitat loss",
            "Overfishing, finning","Commercial whaling legacy","Bycatch, climate change",
            "Overfishing, reef degradation","Overfishing, finning","Ocean warming, bleaching",
        ],
        "conservation_action": [
            "IWC protections","CITES Appendix I","Gulf of California reserve",
            "Dugong conservation MOU","CITES Appendix II","CITES listing, fishing bans",
            "Leatherback recovery programs","Hunting quotas, Arctic treaties","Mekong protected areas",
            "CITES Appendix II","IWC moratorium","Turtle excluder devices",
            "CITES Appendix II","CITES Appendix II","Coral Triangle Initiative",
        ],
        "how_you_can_help": [
            "Support whale-safe shipping policies, donate to ocean noise-reduction campaigns, and choose sustainably sourced seafood to reduce entanglement risks.",
            "Never buy products made from tortoiseshell, support marine protected areas, and volunteer with sea turtle nesting-beach patrols.",
            "Refuse to buy shrimp and fish caught with gillnets in the Upper Gulf of California, and support organizations pushing for a permanent gillnet ban.",
            "Reduce boat speeds in seagrass habitats, support seagrass restoration projects, and report illegal dugong hunting to local authorities.",
            "Never consume shark fin soup, support sustainable fishing certifications, and practice responsible snorkelling and diving around whale sharks.",
            "Advocate for shark-finning bans, support catch-and-release fishing for sharks, and choose MSC-certified seafood.",
            "Reduce plastic use (especially bags and balloons that resemble jellyfish), support beach clean-ups, and back climate-action initiatives.",
            "Reduce your carbon footprint to slow Arctic ice loss, support Indigenous-led conservation programs, and avoid products linked to Arctic drilling.",
            "Avoid tours that chase or crowd dolphins, support community-based river conservation, and reduce plastic waste entering waterways.",
            "Demand shark-finning bans from lawmakers, avoid unsustainably caught tuna, and support marine sanctuaries in the open ocean.",
            "Support the IWC commercial-whaling moratorium, reduce ocean noise pollution awareness, and donate to whale research organizations.",
            "Reduce single-use plastics, volunteer for beach clean-ups during nesting season, and turn off beachfront lights at night to protect hatchlings.",
            "Choose reef-safe sunscreen, never buy humphead wrasse at restaurants, and support marine park enforcement in coral reef regions.",
            "Choose pole-and-line or troll-caught fish, push for international catch limits on mako sharks, and support tagging and research programs.",
            "Use reef-safe sunscreen, reduce carbon emissions to fight ocean warming, and support coral reef restoration and nursery projects.",
        ],
    })

marine_species = load_data()

STATUS_COLORS    = {"Critically Endangered":"red","Endangered":"orange","Vulnerable":"green"}
STATUS_TAG_CLASS = {"Critically Endangered":"tag-cr","Endangered":"tag-en","Vulnerable":"tag-vu"}
STATUS_ICONS     = {"Critically Endangered":"exclamation-sign","Endangered":"warning-sign","Vulnerable":"info-sign"}

with st.sidebar:
    st.markdown("### 🔍 Filter Species")
    selected_statuses = st.multiselect("Threat Status",  sorted(marine_species.status.unique()), default=sorted(marine_species.status.unique()))
    selected_oceans   = st.multiselect("Ocean / Region", sorted(marine_species.ocean.unique()),  default=sorted(marine_species.ocean.unique()))
    st.markdown("---")
    st.markdown("### 🗺️ Map Layers")
    show_clusters = st.checkbox("Species Markers",       value=True)
    show_heatmap  = st.checkbox("Biodiversity Heatmap",  value=True)
    st.markdown("---")
    st.caption("Data is illustrative. Sources: IUCN Red List, WWF, NOAA.")

filtered = marine_species[marine_species.status.isin(selected_statuses) & marine_species.ocean.isin(selected_oceans)]

st.markdown("<h1 class=\'main-title\'>🌊 Endangered Oceans Atlas</h1>", unsafe_allow_html=True)
st.markdown("<p class=\'subtitle\'>Tracking marine species at risk across the world\'s oceans</p>", unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
for col,num,label in [
    (c1, len(filtered), "Species Shown"),
    (c2, len(filtered[filtered.status=="Critically Endangered"]), "Critically Endangered"),
    (c3, len(filtered[filtered.status=="Endangered"]), "Endangered"),
    (c4, len(filtered[filtered.status=="Vulnerable"]), "Vulnerable"),
]:
    col.markdown(f\'<div class="stat-card"><div class="stat-number">{num}</div><div class="stat-label">{label}</div></div>\', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

ocean_map = folium.Map(location=[20,0], zoom_start=2, tiles="CartoDB positron")

if show_heatmap and not filtered.empty:
    HeatMap(filtered[["latitude","longitude"]].values.tolist(), name="Biodiversity Heatmap",
            radius=40, blur=30, gradient={"0.2":"#1a6fa5","0.5":"#f39c12","1.0":"#c0392b"}).add_to(ocean_map)

if show_clusters and not filtered.empty:
    mc = MarkerCluster(name="Species Markers").add_to(ocean_map)
    for _, row in filtered.iterrows():
        bg  = "#ffe0e0" if "Critical" in row.status else "#fff3cd" if "End" in row.status else "#e2f0e8"
        fg  = "#c0392b" if "Critical" in row.status else "#856404" if "End" in row.status else "#1a6b3a"
        popup_html = f"""
        <div style="width:260px;font-family:\'Segoe UI\',sans-serif;">
            <h3 style="color:#0a3d62;margin:0 0 6px 0;">🐋 {row.species_name}</h3>
            <hr style="margin:4px 0;border-color:#cce0f5;">
            <p style="margin:4px 0;"><b>Status:</b>
                <span style="background:{bg};color:{fg};padding:1px 8px;border-radius:999px;font-size:.8em;font-weight:600;">{row.status}</span></p>
            <p style="margin:4px 0;"><b>Ocean:</b> {row.ocean}</p>
            <p style="margin:4px 0;"><b>Population:</b> {row.population_estimate}</p>
            <p style="margin:4px 0;"><b>Threat:</b> {row.primary_threat}</p>
            <p style="margin:4px 0;"><b>Conservation:</b> {row.conservation_action}</p>
            <hr style="margin:6px 0;border-color:#cce0f5;">
            <p style="margin:4px 0;color:#0a3d62;"><b>🤝 How You Can Help:</b></p>
            <p style="margin:4px 0;font-size:.85em;color:#333;">{row.how_you_can_help}</p>
        </div>"""
        folium.Marker(
            location=[row.latitude, row.longitude],
            popup=folium.Popup(popup_html, max_width=320),
            tooltip=f"{row.species_name} — {row.status}",
            icon=folium.Icon(color=STATUS_COLORS.get(row.status,"blue"), icon=STATUS_ICONS.get(row.status,"info-sign")),
        ).add_to(mc)

Fullscreen(position="topleft", title="Full Screen", title_cancel="Exit Full Screen", force_separate_button=True).add_to(ocean_map)
folium.LayerControl(collapsed=False).add_to(ocean_map)

map_col, table_col = st.columns([3,2], gap="medium")
with map_col:
    st.markdown("#### Interactive Map")
    st_folium(ocean_map, width="100%", height=480)
with table_col:
    st.markdown("#### Species in View")
    if filtered.empty:
        st.info("No species match the current filters.")
    else:
        for _, row in filtered.iterrows():
            tc = STATUS_TAG_CLASS.get(row.status,"tag-en")
            with st.expander(f"{row.species_name}  —  {row.status}"):
                st.markdown(f"""
                <div class="species-card">
                    <strong>{row.species_name}</strong><br>
                    <span class="tag {tc}">{row.status}</span>&nbsp;
                    <small style="color:#555">{row.ocean}</small><br>
                    <small>👥 {row.population_estimate}</small><br>
                    <small>⚠️ {row.primary_threat}</small>
                    <hr style="margin:8px 0;border-color:#cce0f5;">
                    <p style="margin:4px 0;color:#0a3d62;font-weight:600;">🤝 How You Can Help</p>
                    <p style="margin:4px 0;font-size:.9em;color:#333;">{row.how_you_can_help}</p>
                </div>""", unsafe_allow_html=True)

st.markdown("---")
l1,l2,l3,_ = st.columns([1,1,1,3])
l1.markdown("🔴 **Critically Endangered**")
l2.markdown("🟠 **Endangered**")
l3.markdown("🟢 **Vulnerable**")
st.caption("Built with Streamlit · folium · streamlit-folium | Data: IUCN Red List, WWF, NOAA")
'''

with open("app.py", "w") as f:
    f.write(app_code)

print("✅ app.py written.")

# ── 3. Start Streamlit in the background ─────────────────────
import subprocess, time

proc = subprocess.Popen(
    ["streamlit", "run", "app.py",
     "--server.port", "8501",
     "--server.headless", "true",
     "--server.enableCORS", "false",
     "--server.enableXsrfProtection", "false"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)

time.sleep(5)   # wait for server to boot
print("✅ Streamlit server started.")

# ── 4. Expose via ngrok → get public URL ─────────────────────
from pyngrok import ngrok

# If you have an ngrok account, paste your auth token here for longer sessions:
ngrok.set_auth_token("36TMIayOSkUmT6CqhjSlUt6CD5i_3qTDwiPov3NZputBvEF1g")

public_url = ngrok.connect(8501)
print("=" * 55)
print(f"  🌊  Endangered Oceans Atlas is LIVE!")
print(f"  👉  {public_url}")
print("=" * 55)
print("  Keep this cell running to stay online.")
print("  Re-run the cell if the URL expires.")


