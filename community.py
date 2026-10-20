"""Small-volume GitHub-backed submissions; no local persistence or public drafts."""
import base64
import csv
import io
import json
import re
import uuid
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

import requests

CONTENT = Path(__file__).parent / "content"
ROLES = ["Science educator", "Professor", "Student", "Researcher", "Other"]


class StorageError(Exception):
    pass


def month_now():
    return datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m")


def read_content(name):
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


def safe_url(url):
    parsed = urlparse(url)
    return parsed.scheme == "https" and bool(parsed.hostname) and not parsed.username


def make_submission(month, question, name, role, institution, answer, consent):
    if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", month):
        raise ValueError("Invalid month")
    name, institution, answer = name.strip(), institution.strip(), answer.strip()
    if not 2 <= len(name) <= 100 or not 20 <= len(answer) <= 5000:
        raise ValueError("Enter a name (2–100 characters) and answer (20–5,000 characters).")
    if role not in ROLES or len(institution) > 150 or not consent or not question:
        raise ValueError("Check your role, institution and publication consent.")
    return dict(id=uuid.uuid4().hex, month=month, question=question, name=name,
                role=role, institution=institution, answer=answer, consent=True,
                status="pending", submitted_at=datetime.now(ZoneInfo("Asia/Kolkata")).isoformat())


def export_answers(records):
    out = io.StringIO()
    fields = ["id", "month", "question", "name", "role", "institution", "answer", "status", "submitted_at"]
    writer = csv.DictWriter(out, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for record in records:
        # Prevent spreadsheet formula execution when opening the editorial export.
        writer.writerow({k: "'" + str(record.get(k, "")) if str(record.get(k, "")).lstrip().startswith(("=", "+", "-", "@")) else record.get(k, "") for k in fields})
    return out.getvalue().encode("utf-8-sig")


class GitHubStore:
    def __init__(self, config):
        self.repo = config.get("repository", "")
        self.token = config.get("token", "")
        self.branch = config.get("branch", "main")
        if not re.fullmatch(r"[\w.-]+/[\w.-]+", self.repo) or not self.token:
            raise StorageError("Contribution storage is not configured yet.")
        self.base = f"https://api.github.com/repos/{self.repo}"
        # Refuse to store pending contributions in a public repository.
        if not self.request("GET", "").json().get("private"):
            raise StorageError("Contribution storage must use a private repository.")

    def request(self, method, path, **kwargs):
        try:
            response = requests.request(method, self.base + path, headers={
                "Authorization": f"Bearer {self.token}", "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28"}, timeout=20, **kwargs)
        except requests.RequestException:
            raise StorageError("Storage is temporarily unavailable. Please try again.") from None
        if response.status_code not in ((200, 201, 404, 409, 422) if method == "PUT" else (200, 404)):
            raise StorageError("Storage request failed. An editor should check repository access; retry later.")
        return response

    def records(self, month):
        if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", month):
            raise StorageError("Invalid month.")
        response = self.request("GET", f"/contents/submissions/{month}", params={"ref": self.branch})
        if response.status_code == 404:
            return []
        entries = response.json()
        if not isinstance(entries, list) or len(entries) >= 1000:
            raise StorageError("This archive requires a storage upgrade before it can be listed safely.")
        records = []
        for entry in entries:
            if entry.get("type") != "file" or not entry["name"].endswith(".json"):
                continue
            response = self.request("GET", f"/contents/{entry['path']}", params={"ref": self.branch})
            if response.status_code == 404:
                raise StorageError("An answer changed while loading. Please refresh.")
            obj = response.json()
            record = json.loads(base64.b64decode(obj["content"]))
            record["_sha"] = obj["sha"]
            records.append(record)
        return sorted(records, key=lambda r: r["submitted_at"], reverse=True)

    def save(self, record):
        payload = {k: v for k, v in record.items() if not k.startswith("_")}
        path = f"submissions/{record['month']}/{record['id']}.json"
        body = dict(message=f"Save contribution {record['id']}", branch=self.branch,
                    content=base64.b64encode(json.dumps(payload, ensure_ascii=False).encode()).decode())
        if record.get("_sha"):
            body["sha"] = record["_sha"]
        response = self.request("PUT", f"/contents/{path}", json=body)
        if response.status_code not in (200, 201):
            if not record.get("_sha") and response.status_code in (409, 422):
                existing = self.request("GET", f"/contents/{path}", params={"ref": self.branch})
                if existing.status_code == 200:
                    obj = existing.json()
                    if json.loads(base64.b64decode(obj["content"])) == payload:
                        record["_sha"] = obj["sha"]
                        return
            raise StorageError("Answer was not saved or changed in another session. Refresh and retry.")
        record["_sha"] = response.json()["content"]["sha"]
