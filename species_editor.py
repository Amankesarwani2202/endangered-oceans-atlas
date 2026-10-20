"""Species authoring UI, called only after the Editor page authenticates."""
from datetime import date
import streamlit as st
from community import GitHubStore, StorageError
from species_catalog import STATUSES, read_catalog, merge_species, publish_species


def render_species_editor(config):
    st.subheader("Manage species")
    st.write("Add a researched animal profile whenever you are ready. Publishing makes it available across the atlas.")
    try:
        store = GitHubStore(config)
        # Keep the exact snapshot the editor saw, including its SHA, across form submission.
        scope = (store.repo, store.branch)
        if st.session_state.get("catalog_scope") != scope:
            st.session_state.pop("species_catalog", None)
            st.session_state.catalog_scope = scope
        if st.button("Reload catalogue"):
            st.session_state.pop("species_catalog", None)
        if "species_catalog" not in st.session_state:
            st.session_state.species_catalog = read_catalog(store)
        additions, sha = st.session_state.species_catalog
        profiles = merge_species(additions)
        st.caption(f"{len(profiles)} published profiles · {len(additions)} added through Editor")
        st.dataframe([{ "Species": r["species_name"], "Status": r["status"], "Ocean / region": r["ocean"]} for r in profiles], hide_index=True, use_container_width=True)
        if st.session_state.pop("species_published", False):
            st.success("Species published. It will appear in Home, Map, Species and Analysis when those pages are opened or refreshed.")
        with st.form("new_species", clear_on_submit=False):
            st.markdown("### New animal profile")
            name = st.text_input("Species name", max_chars=120)
            emoji = st.text_input("Animal emoji", value="🐟", max_chars=16)
            status = st.selectbox("Conservation status", STATUSES)
            ocean = st.text_input("Ocean / region", max_chars=120)
            a, b = st.columns(2)
            latitude = a.number_input("Latitude", min_value=-90.0, max_value=90.0, value=0.0, format="%.4f")
            longitude = b.number_input("Longitude", min_value=-180.0, max_value=180.0, value=0.0, format="%.4f")
            st.caption("Choose a representative location in its habitat. This marker does not represent its full range.")
            population = st.text_input("Population estimate (include scope / date, or Unknown)", max_chars=200)
            threat = st.text_area("Primary threats", max_chars=1000)
            action = st.text_area("Conservation actions", max_chars=1000)
            help_text = st.text_area("How visitors can help", max_chars=2000)
            fact = st.text_area("Fun fact", max_chars=2000)
            source = st.text_input("Source link (HTTPS)", placeholder="https://www.iucnredlist.org/...", max_chars=2000)
            reviewed = st.date_input("Source reviewed on", value=date.today(), max_value=date.today())
            verified = st.checkbox("I have checked the status, population, location and facts against reliable sources and want to publish this profile.")
            submitted = st.form_submit_button("Publish species")
        if submitted:
            try:
                if not verified:
                    raise ValueError("Check the research confirmation before publishing.")
                record = dict(species_name=name, emoji=emoji, status=status, ocean=ocean,
                              latitude=latitude, longitude=longitude, population_estimate=population,
                              primary_threat=threat, conservation_action=action, how_you_can_help=help_text,
                              fun_fact=fact, source_url=source, last_reviewed=reviewed.isoformat())
                updated = publish_species(store, record, additions, sha)
                st.session_state.species_catalog = updated
                st.session_state.species_published = True
                st.rerun()
            except (StorageError, ValueError) as exc:
                st.error(str(exc))
    except (StorageError, ValueError) as exc:
        st.error(str(exc))
