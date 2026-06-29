# 🌊 Endangered Oceans Atlas

A multi-page Streamlit app tracking 15 marine species at risk across the world's oceans.

## Pages

| Page | Description |
|------|-------------|
| 🏠 Home | Landing page with key stats, navigation cards, and quick facts |
| 🗺️ Map | Interactive folium map with clustering, heatmap, and species popups |
| 📋 Species | Card or table directory with filters and detailed profiles |
| 📊 Analysis | Charts: status distribution, ocean breakdown, threat categories, heatmap |

## Deploy to Streamlit Cloud

1. **Push this folder to a GitHub repository** (public or private).

2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in.

3. Click **New app** and fill in:
   - **Repository:** `your-username/your-repo`
   - **Branch:** `main`
   - **Main file path:** `Home.py`

4. Click **Deploy** — Streamlit Cloud will install `requirements.txt` automatically.

## Local development

```bash
pip install -r requirements.txt
streamlit run Home.py
```

## Project structure

```
endangered-oceans/
├── Home.py                  # Landing / home page
├── data.py                  # Shared dataset + constants
├── requirements.txt
├── .streamlit/
│   └── config.toml          # Theme + server settings
└── pages/
    ├── 1_🗺️_Map.py
    ├── 2_📋_Species.py
    └── 3_📊_Analysis.py
```

## Data sources

Data is illustrative and compiled from:
- [IUCN Red List](https://www.iucnredlist.org/)
- [WWF](https://www.worldwildlife.org/)
- [NOAA Fisheries](https://www.fisheries.noaa.gov/)