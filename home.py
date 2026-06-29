import streamlit as st

st.set_page_config(
    page_title="🌊 Endangered Oceans Atlas",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: "Inter", sans-serif;
}

/* ── Hero ── */
.hero {
    background: linear-gradient(160deg, #020e1f 0%, #0a3d62 55%, #0e5fa3 100%);
    border-radius: 20px;
    padding: 4rem 3rem 3.5rem;
    position: relative;
    overflow: hidden;
    margin-bottom: 2rem;
}
.hero::before {
    content: "";
    position: absolute;
    inset: 0;
    background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='900' height='300'%3E%3Cellipse cx='750' cy='150' rx='320' ry='220' fill='%230e5fa3' opacity='.25'/%3E%3Cellipse cx='100' cy='250' rx='180' ry='120' fill='%231a6fa5' opacity='.18'/%3E%3C/svg%3E") no-repeat right center;
    background-size: cover;
    pointer-events: none;
}
.hero-eyebrow {
    font-size: .8rem;
    font-weight: 600;
    letter-spacing: .18em;
    text-transform: uppercase;
    color: #5bc8f5;
    margin-bottom: .6rem;
}
.hero-title {
    font-family: "Playfair Display", serif;
    font-size: clamp(2.4rem, 5vw, 3.8rem);
    font-weight: 900;
    color: #ffffff;
    line-height: 1.1;
    margin: 0 0 1rem;
}
.hero-title span { color: #5bc8f5; }
.hero-subtitle {
    font-size: 1.1rem;
    font-weight: 300;
    color: #a8d4f0;
    max-width: 540px;
    line-height: 1.65;
    margin-bottom: 2rem;
}
.hero-badge {
    display: inline-block;
    padding: .35rem .9rem;
    border: 1px solid rgba(91,200,245,.35);
    border-radius: 999px;
    font-size: .78rem;
    color: #5bc8f5;
    margin-right: .5rem;
    margin-bottom: .4rem;
    backdrop-filter: blur(4px);
}

/* ── Stat strip ── */
.stat-strip {
    display: flex;
    gap: 1px;
    background: #d0e8f7;
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 2.4rem;
}
.stat-cell {
    flex: 1;
    background: #f0f8ff;
    padding: 1.2rem 1rem;
    text-align: center;
}
.stat-cell:first-child { border-radius: 14px 0 0 14px; }
.stat-cell:last-child  { border-radius: 0 14px 14px 0; }
.stat-num {
    font-family: "Playfair Display", serif;
    font-size: 2.1rem;
    font-weight: 700;
    color: #0a3d62;
    line-height: 1;
}
.stat-lbl {
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: #4a6fa5;
    margin-top: .3rem;
}

/* ── Nav cards ── */
.nav-grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(240px,1fr)); gap: 1.2rem; margin-bottom: 2.4rem; }
.nav-card {
    background: #ffffff;
    border: 1px solid #d0e4f5;
    border-radius: 16px;
    padding: 1.6rem 1.4rem;
    text-decoration: none;
    transition: box-shadow .2s, transform .2s;
    cursor: pointer;
}
.nav-card:hover { box-shadow: 0 6px 24px rgba(10,61,98,.13); transform: translateY(-3px); }
.nav-icon { font-size: 2rem; margin-bottom: .7rem; }
.nav-title { font-size: 1.05rem; font-weight: 600; color: #0a3d62; margin-bottom: .3rem; }
.nav-desc  { font-size: .85rem; color: #5a7fa0; line-height: 1.5; }

/* ── Crisis callout ── */
.crisis-bar {
    background: linear-gradient(90deg,#c0392b,#e74c3c);
    color: white;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    font-size: .9rem;
    font-weight: 500;
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    gap: .8rem;
}

/* ── Footer ── */
.footer {
    text-align: center;
    color: #7a9ab5;
    font-size: .78rem;
    padding: 1.5rem 0 .5rem;
    border-top: 1px solid #d0e4f5;
}

div[data-testid="stSidebar"] { background: #f5f9ff; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">IUCN Red List · WWF · NOAA</div>
  <h1 class="hero-title">Endangered<br><span>Oceans Atlas</span></h1>
  <p class="hero-subtitle">
    A living reference for the marine species slipping toward extinction —
    where they live, why they're at risk, and what each of us can do today.
  </p>
  <span class="hero-badge">🔴 Critically Endangered</span>
  <span class="hero-badge">🟠 Endangered</span>
  <span class="hero-badge">🟢 Vulnerable</span>
</div>
""", unsafe_allow_html=True)

# ── Crisis callout ────────────────────────────────────────────
st.markdown("""
<div class="crisis-bar">
  🚨 <strong>Ocean Crisis:</strong>&nbsp;
  More than <strong>33 % of assessed marine species</strong> face elevated extinction risk.
  Plastic pollution, climate change, overfishing, and habitat destruction are the leading drivers.
</div>
""", unsafe_allow_html=True)

# ── Stat strip ────────────────────────────────────────────────
st.markdown("""
<div class="stat-strip">
  <div class="stat-cell"><div class="stat-num">15</div><div class="stat-lbl">Species Tracked</div></div>
  <div class="stat-cell"><div class="stat-num">6</div><div class="stat-lbl">Critically Endangered</div></div>
  <div class="stat-cell"><div class="stat-num">7</div><div class="stat-lbl">Endangered</div></div>
  <div class="stat-cell"><div class="stat-num">2</div><div class="stat-lbl">Vulnerable</div></div>
  <div class="stat-cell"><div class="stat-num">5</div><div class="stat-lbl">Ocean Regions</div></div>
</div>
""", unsafe_allow_html=True)

# ── Navigation cards ──────────────────────────────────────────
st.markdown("### Explore the Atlas")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="nav-card">
      <div class="nav-icon">🗺️</div>
      <div class="nav-title">Interactive Map</div>
      <div class="nav-desc">Explore species locations on a global map with clustering, heat-map overlays, and detailed pop-ups for each animal.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Map →", key="map_btn", use_container_width=True):
        st.switch_page("pages/1_🗺️_Map.py")

with col2:
    st.markdown("""
    <div class="nav-card">
      <div class="nav-icon">📋</div>
      <div class="nav-title">Species Directory</div>
      <div class="nav-desc">Browse all 15 tracked species, filter by threat status or ocean region, and read detailed conservation profiles.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Browse Species →", key="dir_btn", use_container_width=True):
        st.switch_page("pages/2_📋_Species.py")

with col3:
    st.markdown("""
    <div class="nav-card">
      <div class="nav-icon">📊</div>
      <div class="nav-title">Threat Analysis</div>
      <div class="nav-desc">Charts and breakdowns of threat categories, ocean-region exposure, and population estimates across all species.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("View Analysis →", key="ana_btn", use_container_width=True):
        st.switch_page("pages/3_📊_Analysis.py")

# ── Quick facts ───────────────────────────────────────────────
st.markdown("---")
st.markdown("### Did You Know?")

facts = [
    ("🐋", "Blue Whales", "The largest animal ever to live on Earth, blue whales number only 10,000–25,000 today — down from hundreds of thousands before commercial whaling."),
    ("🐢", "Hawksbill Turtle", "Critically endangered due to demand for its beautiful shell. Even a single tortoiseshell product purchased funds the poaching trade."),
    ("🦈", "Vaquita Porpoise", "Fewer than 10 individuals remain, making the vaquita the world's most critically endangered marine mammal — and possibly already beyond saving."),
    ("🪸", "Staghorn Coral", "This reef-building coral has declined to less than 1 % of its 1980s abundance due to ocean warming and bleaching events."),
]

cols = st.columns(2)
for i, (icon, name, text) in enumerate(facts):
    with cols[i % 2]:
        st.markdown(f"""
        <div style="background:#f0f8ff;border-left:4px solid #1a6fa5;border-radius:0 12px 12px 0;
                    padding:.9rem 1.1rem;margin-bottom:1rem;">
          <div style="font-size:1.4rem;margin-bottom:.3rem;">{icon} <strong style="color:#0a3d62">{name}</strong></div>
          <div style="font-size:.88rem;color:#3a5f7a;line-height:1.55">{text}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  Built with Streamlit · folium · streamlit-folium &nbsp;|&nbsp;
  Data: IUCN Red List, WWF, NOAA &nbsp;|&nbsp;
  Data is illustrative and for educational purposes.
</div>
""", unsafe_allow_html=True)