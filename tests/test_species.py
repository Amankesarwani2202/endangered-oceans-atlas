import base64
import json
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
from datetime import date
from streamlit.testing.v1 import AppTest
from community import StorageError
from species_catalog import merge_species, validate_species, publish_species, read_catalog

ROOT = Path(__file__).resolve().parents[1]


def record():
    return dict(species_name="Test marine animal", emoji="🐟", status="Endangered", ocean="Test Ocean",
                latitude=12.0, longitude=34.0, population_estimate="Unknown", primary_threat="Habitat loss",
                conservation_action="Protect habitat", how_you_can_help="Support habitat restoration",
                fun_fact="A test profile for automated checks only.", source_url="https://example.org/species",
                last_reviewed=date.today().isoformat())


def response(status, obj):
    r = Mock(status_code=status)
    r.json.return_value = obj
    return r


class SpeciesTests(unittest.TestCase):
    def test_validation_duplicates_and_originals(self):
        self.assertEqual(len(merge_species([])), 15)
        self.assertEqual(len(merge_species([record()])), 16)
        for field, value in [("latitude", float("nan")), ("longitude", 181), ("source_url", "javascript:alert(1)"), ("species_name", ""), ("status", "anything")]:
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_species({**record(), field: value}, require_source=True)
        with self.assertRaises(ValueError):
            merge_species([{**record(), "species_name": " blue   whale "}])

    def test_stale_write_does_not_overwrite(self):
        store = Mock(branch="main")
        current = [{**record(), "species_name": "Other animal"}]
        store.request.side_effect = [response(409, {}), response(200, {"content": base64.b64encode(json.dumps(current).encode()).decode(), "sha": "new"})]
        with self.assertRaises(StorageError):
            publish_species(store, record(), [], "old")
        self.assertEqual(store.request.call_args_list[0].kwargs["json"]["sha"], "old")
        self.assertEqual(len([c for c in store.request.call_args_list if c.args[0] == "PUT"]), 1)

    @patch("community.requests.request")
    def test_editor_publish_persists_across_new_page_sessions(self, request):
        additions = []
        sha = None
        def api(method, url, **kwargs):
            nonlocal additions, sha
            if method == "PUT":
                additions = json.loads(base64.b64decode(kwargs["json"]["content"]))
                sha = "saved"
                return response(201, {"content": {"sha": sha}})
            if url.endswith("/repos/a/b"):
                return response(200, {"private": True})
            if "/branches/" in url:
                return response(200, {"name": "main"})
            if url.endswith("/atlas/species.json") and sha:
                return response(200, {"content": base64.b64encode(json.dumps(additions).encode()).decode(), "sha": sha})
            return response(404, {})
        request.side_effect = api
        config = {"repository": "a/b", "token": "test", "editor_password": "test-password"}
        editor = AppTest.from_file(str(ROOT / "pages/6_Editor.py"))
        editor.secrets["community"] = config
        editor.run()
        editor.text_input[0].set_value("test-password")
        editor.button[0].click().run()
        editor.radio[0].set_value("Manage species").run()
        self.assertEqual(list(editor.exception), [])
        values = {"Species name": record()["species_name"], "Ocean / region": "Test Ocean",
                  "Population estimate (include scope / date, or Unknown)": "Unknown", "Source link (HTTPS)": "https://example.org/species"}
        for widget in editor.text_input:
            if widget.label in values:
                widget.set_value(values[widget.label])
        for widget in editor.text_area:
            widget.set_value("Researched descriptive information.")
        editor.checkbox[0].check()
        next(b for b in editor.button if b.label == "Publish species").click().run()
        self.assertEqual(list(editor.exception), [])
        self.assertTrue(editor.success)
        self.assertEqual(len(additions), 1)
        # Separate page sessions read persisted content; no local state or cache needed.
        for page in ["Home.py", "pages/2_📋_Species.py", "pages/3_📊_Analysis.py", "pages/1_🗺️_Map.py"]:
            with self.subTest(page=page):
                app = AppTest.from_file(str(ROOT / page))
                app.secrets["community"] = config
                app.run(timeout=30)
                self.assertEqual(list(app.exception), [])
                if page == "Home.py":
                    self.assertEqual(app.metric[0].value, "16")
                elif "Species" in page:
                    self.assertTrue(any(record()["species_name"] in m.value for m in app.markdown))
                elif "Map" in page:
                    self.assertTrue(any(record()["species_name"] in e.label for e in app.expander))
                else:
                    # The status data used by all charts contains the new animal.
                    from data import load_data
                    with patch("data.st.secrets", {"community": config}):
                        self.assertEqual(len(load_data()), 16)
        # The second publish from a stale snapshot is prevented by duplicate validation.
        with self.assertRaises(ValueError):
            publish_species(Mock(), additions[0], additions, sha)

    @patch("community.requests.request")
    def test_unavailable_storage_warns_and_keeps_atlas(self, request):
        import requests
        request.side_effect = requests.ConnectionError()
        app = AppTest.from_file(str(ROOT / "Home.py"))
        app.secrets["community"] = {"repository": "a/b", "token": "test"}
        app.run()
        self.assertEqual(list(app.exception), [])
        self.assertTrue(app.warning)
        self.assertEqual(app.metric[0].value, "15")
