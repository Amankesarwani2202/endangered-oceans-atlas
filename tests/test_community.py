import base64
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
from unittest.mock import Mock, patch
from community import GitHubStore, StorageError, make_submission, export_answers
from streamlit.testing.v1 import AppTest


def response(status, data):
    result = Mock(status_code=status)
    result.json.return_value = data
    return result


class CommunityTests(unittest.TestCase):
    def record(self):
        return make_submission("2026-10", "Question?", "Aman", "Researcher", "", "Protect coastal habitats through local action.", True)

    def test_validation_and_consent(self):
        r = self.record()
        self.assertEqual(r["status"], "pending")
        with self.assertRaises(ValueError):
            make_submission("2026-10", "Q", "Aman", "Student", "", "A sufficiently detailed answer.", False)
        self.assertTrue(export_answers([{**r, "name": "=1+1"}]).decode("utf-8-sig").find("'=1+1") > 0)

    @patch("community.requests.request")
    def test_private_store_and_conflict(self, request):
        request.return_value = response(200, {"private": False})
        with self.assertRaises(StorageError):
            GitHubStore({"repository": "a/b", "token": "test"})
        request.return_value = response(200, {"private": True})
        store = GitHubStore({"repository": "a/b", "token": "test"})
        record = self.record()
        request.return_value = response(201, {"content": {"sha": "first"}})
        store.save(record)
        self.assertEqual(record["_sha"], "first")
        request.return_value = response(409, {})
        with self.assertRaises(StorageError):
            store.save(record)

    @patch("community.requests.request")
    def test_timeout_retry_same_record(self, request):
        request.return_value = response(200, {"private": True})
        store = GitHubStore({"repository": "a/b", "token": "test"})
        record = self.record()
        encoded = base64.b64encode(json.dumps(record).encode()).decode()
        request.side_effect = [response(422, {}), response(200, {"content": encoded, "sha": "already-saved"})]
        store.save(record)
        self.assertEqual(record["_sha"], "already-saved")

    def test_pages_without_secrets(self):
        for path in ["Home.py", "pages/4_Contributors.py", "pages/5_Newsletters.py", "pages/6_Editor.py"]:
            with self.subTest(path=path):
                app = AppTest.from_file(str(ROOT / path)).run(timeout=20)
                self.assertEqual(list(app.exception), [])

    @patch("community.requests.request")
    def test_contributor_submission_is_pending(self, request):
        def api(method, url, **kwargs):
            if method == "PUT":
                return response(201, {"content": {"sha": "saved"}})
            if url.endswith("/repos/a/b"):
                return response(200, {"private": True})
            return response(404, {})
        request.side_effect = api
        app = AppTest.from_file(str(ROOT / "pages/4_Contributors.py"))
        app.secrets["community"] = {"repository": "a/b", "token": "test"}
        app.run()
        app.text_input[0].set_value("Aman")
        app.text_area[0].set_value("Protect coastal habitats through local action.")
        app.checkbox[0].check()
        app.button[0].click().run()
        self.assertEqual(list(app.exception), [])
        self.assertTrue(app.success)
        writes = [c for c in request.call_args_list if c.args[0] == "PUT"]
        payload = json.loads(base64.b64decode(writes[-1].kwargs["json"]["content"]))
        self.assertEqual(payload["status"], "pending")
        self.assertFalse(any(t.value == payload["answer"] for t in app.text))

    @patch("community.requests.request")
    def test_submit_approve_feed_and_export(self, request):
        record = self.record()
        encoded = lambda r: base64.b64encode(json.dumps(r).encode()).decode()
        def api(method, url, **kwargs):
            if url.endswith("/repos/a/b"):
                return response(200, {"private": True})
            if method == "PUT":
                return response(200, {"content": {"sha": "updated"}})
            if url.endswith("/2026-10"):
                return response(200, [{"type": "file", "name": record["id"] + ".json", "path": "submissions/2026-10/answer.json"}])
            return response(200, {"content": encoded(record), "sha": "original"})
        request.side_effect = api
        config = {"repository": "a/b", "token": "test", "editor_password": "test-password"}
        app = AppTest.from_file(str(ROOT / "pages/6_Editor.py"))
        app.secrets["community"] = config
        app.run()
        app.text_input[0].set_value("test-password")
        app.button[0].click().run()
        self.assertEqual(list(app.exception), [])
        app.selectbox(key=record["id"]).set_value("approved")
        app.button(key="save_" + record["id"]).click().run()
        writes = [c for c in request.call_args_list if c.args[0] == "PUT"]
        payload = json.loads(base64.b64decode(writes[-1].kwargs["json"]["content"]))
        self.assertEqual(payload["status"], "approved")
        record["status"] = "approved"
        feed = AppTest.from_file(str(ROOT / "pages/4_Contributors.py"))
        feed.secrets["community"] = config
        feed.run()
        self.assertEqual(list(feed.exception), [])
        self.assertTrue(any(t.value == record["answer"] for t in feed.text))

if __name__ == "__main__":
    unittest.main()
