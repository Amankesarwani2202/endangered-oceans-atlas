"""Run page tests through the real multipage entrypoint so links can resolve."""
from pathlib import Path
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


def atlas_app(path):
    path = Path(path)
    relative = path.relative_to(ROOT) if path.is_absolute() else path
    app = AppTest.from_file(str(ROOT / "Home.py"))
    if str(relative) != "Home.py":
        app.run(timeout=30)
        app.switch_page(str(relative))
    return app
