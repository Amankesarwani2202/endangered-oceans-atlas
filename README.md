# 🌊 Endangered Oceans Atlas

A gentle, student-friendly guide to the Endangered Oceans Atlas — a small interactive web app that shows where threatened marine species live, why they're at risk, and how people can help.

## What is this project?
- It's a multi-page Streamlit app (a simple Python web app) that includes:
  - An interactive map with species markers and a heatmap.
  - A species directory with short profiles.
  - A threat analysis page with charts.

This is meant as an educational tool and example project for learning data, maps, and simple web apps.

## Why this is useful for a 10th-grade scholar
- Learn how data can be shown on maps and charts.
- See real conservation problems (overfishing, pollution, climate change) with simple visuals.
- Try editing the data and immediately see the results in the app — a quick way to learn coding and data thinking.

## Quick setup (step-by-step)
1. Install Python 3.8+ if you don't have it.
2. Open a terminal (or command prompt) and install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app locally:

```bash
streamlit run Home.py
```

4. Your browser should open a local page (usually at `http://localhost:8501`). Use the navigation on the Home page to open Map, Species, and Analysis pages.

## How the app is organized (simple terms)
- `Home.py` — The front page of the app where you can navigate to other pages.
- `pages/1_🗺️_Map.py` — Shows the interactive folium map with markers and a heatmap. Click markers to read species details.
- `pages/2_📋_Species.py` — A directory of species shown as cards or a table with filters.
- `pages/3_📊_Analysis.py` — Charts that summarize threats and where species are found.
- `data.py` — The small dataset and shared colors/constants. The function `load_data()` returns a pandas DataFrame the pages use.
- `.gitignore` — Tells git to ignore cache files like `__pycache__`.

## How to read and change the data (easy example)
1. Open `data.py` in a text editor.
2. Find the `load_data()` function — it returns a table (a list of species and fields like `species_name`, `latitude`, `longitude`, `status`).
3. To add a new species, add another entry in the lists, for example:

```python
# inside load_data()
"species_name": ["Blue Whale", "New Turtle"],
"latitude": [-33.86, 12.34],
"longitude": [151.20, 45.67],
"status": ["Endangered", "Vulnerable"],
```

4. Save the file and refresh the Streamlit app in the browser. The new species should appear.

## Interacting with the app
- Use the sidebar filters to narrow species by threat status or ocean region.
- On the Map page, toggle the heatmap and marker clusters to change the visualization.
- The Analysis page uses Plotly for nicer charts; if Plotly is not installed it falls back to basic Streamlit charts.

## Troubleshooting (common problems)
- "ModuleNotFoundError": run `pip install -r requirements.txt` again.
- Browser doesn't open: check the terminal for the URL `http://localhost:8501` and open it manually.
- If edits don't appear: press the browser refresh button or restart Streamlit.

## For sharing and deployment
- To share with others, push this repo to GitHub and use Streamlit Community Cloud (share.streamlit.io) or host on any server that can run Streamlit.
- For Streamlit Cloud, set the main file as `Home.py` when creating the app.

## How to contribute (simple workflow)
1. Make a new branch: `git checkout -b feature/my-change`
2. Edit or add code.
3. Commit: `git add . && git commit -m "Add X"`
4. Push and open a pull request on GitHub.

## Notes for teachers / mentors
- The project is intentionally small and uses static example data. It's a safe sandbox for students to:
  - Edit the dataset in `data.py` and see app changes.
  - Add simple pages in the `pages/` folder.
  - Explore mapping concepts with `folium` and basic charting.

## License & credits
- Data in this example is illustrative only. Credit: IUCN Red List, WWF, NOAA (sampled for educational purposes).

---
If you'd like, I can:
- add this README to the repo (I can commit it now), or
- create a shorter printable one-page summary for your scholar.
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