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
    return pd.DataFrame({
        "species_name": [
            "Blue Whale", "Hawksbill Turtle", "Vaquita", "Dugong", "Whale Shark",
            "Great Hammerhead Shark", "Leatherback Turtle", "Narwhal",
            "Irrawaddy Dolphin", "Oceanic Whitetip Shark", "Sei Whale",
            "Green Turtle", "Humphead Wrasse", "Shortfin Mako Shark", "Staghorn Coral",
        ],
        "emoji": ["🐋","🐢","🐬","🦭","🦈","🦈","🐢","🦄","🐬","🦈","🐋","🐢","🐟","🦈","🪸"],
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
        "fun_fact": [
            "Blue whales can produce sounds louder than a jet engine — up to 188 decibels — heard across entire ocean basins.",
            "Hawksbill turtles are one of the few animals that can eat toxic sea sponges that other species avoid.",
            "The vaquita was only discovered in 1958 and may be extinct within this decade.",
            "Dugongs can live over 70 years and are thought to be the origin of ancient mermaid legends.",
            "Whale sharks are filter feeders that can live over 100 years and are the world's largest fish.",
            "Great hammerheads use their oddly shaped heads like a metal detector to find stingrays buried in sand.",
            "Leatherbacks can dive deeper than 1,200 m and travel over 10,000 km on a single migration.",
            "Narwhals' spiral tusks are actually teeth — they can grow up to 3 metres long.",
            "Irrawaddy dolphins cooperate with fishermen, herding fish into nets in exchange for a share of the catch.",
            "Oceanic whitetip sharks were once described as the most abundant large animal on Earth. Now they're critically endangered.",
            "Sei whales are among the fastest cetaceans, capable of bursts up to 50 km/h.",
            "Green turtles navigate thousands of kilometres to lay eggs on the exact beach where they were born.",
            "Humphead wrasse can live 30+ years and change sex from female to male as they age.",
            "Shortfin mako sharks can leap up to 6 metres out of the water when hooked.",
            "A single staghorn coral colony can grow several centimetres per year — but bleaching can kill it overnight.",
        ],
    })