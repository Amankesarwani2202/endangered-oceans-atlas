import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


class NavigationTests(unittest.TestCase):
    def test_sidebar_survives_navigation_to_every_page(self):
        app = AppTest.from_file(str(ROOT / "Home.py")).run()
        paths = ["Home.py"] + [str(p.relative_to(ROOT)) for p in sorted((ROOT / "pages").glob("*.py"))]
        for path in paths:
            with self.subTest(path=path):
                app.switch_page(path).run(timeout=30)
                self.assertEqual(list(app.exception), [])
                links = app.sidebar.get("page_link")
                self.assertEqual([l.proto.label for l in links], ["Home", "Map", "Species", "Analysis", "Contributors", "Newsletters", "Editor"])
                self.assertTrue(all(l.proto.icon for l in links))
