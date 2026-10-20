"""Validated, editor-published species additions in the private data repository."""
import base64
import copy
import json
import math
import unicodedata
from datetime import date, datetime
from community import StorageError, read_content, safe_url

CATALOG_PATH = "atlas/species.json"
STATUSES = ["Critically Endangered", "Endangered", "Vulnerable"]
TEXT_LIMITS = {"species_name": 120, "emoji": 16, "ocean": 120,
               "population_estimate": 200, "primary_threat": 1000,
               "conservation_action": 1000, "how_you_can_help": 2000, "fun_fact": 2000}


def species_key(name):
    return " ".join(unicodedata.normalize("NFKC", name).casefold().split())


def validate_species(record, require_source=False):
    if not isinstance(record, dict):
        raise ValueError("A species profile must be an object.")
    result = copy.deepcopy(record)
    for field, limit in TEXT_LIMITS.items():
        value = result.get(field)
        if not isinstance(value, str) or not value.strip() or len(value.strip()) > limit:
            raise ValueError(f"Enter {field.replace('_', ' ')} (1–{limit} characters).")
        result[field] = value.strip()
    if result.get("status") not in STATUSES:
        raise ValueError("Choose a supported conservation status.")
    for field, limit in [("latitude", 90), ("longitude", 180)]:
        value = result.get(field)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or abs(value) > limit:
            raise ValueError(f"{field.capitalize()} must be between {-limit} and {limit}.")
    if require_source or result.get("source_url"):
        url = result.get("source_url", "")
        if not isinstance(url, str) or len(url) > 2000 or not safe_url(url):
            raise ValueError("Enter an HTTPS source link, such as an IUCN or NOAA species profile.")
        try:
            reviewed = date.fromisoformat(result.get("last_reviewed", ""))
        except (TypeError, ValueError):
            raise ValueError("Enter a valid source review date.") from None
        if reviewed > date.today():
            raise ValueError("The source review date cannot be in the future.")
    return result


def merge_species(additions):
    if not isinstance(additions, list):
        raise ValueError("Species additions must be a list.")
    rows = [validate_species(r) for r in read_content("species.json")]
    seen = {species_key(r["species_name"]) for r in rows}
    for entry in additions:
        row = validate_species(entry, require_source=True)
        key = species_key(row["species_name"])
        if key in seen:
            raise ValueError(f"A profile already exists for {row['species_name']}.")
        rows.append(row)
        seen.add(key)
    return rows


def read_catalog(store):
    response = store.request("GET", f"/contents/{CATALOG_PATH}", params={"ref": store.branch})
    if response.status_code == 404:
        # A missing file is expected only before the first publication.
        branch = store.request("GET", "/branches/" + store.branch)
        if branch.status_code != 200:
            raise StorageError("The data repository branch is unavailable.")
        return [], None
    try:
        obj = response.json()
        additions = json.loads(base64.b64decode(obj["content"]))
        merge_species(additions)
        return additions, obj["sha"]
    except (KeyError, TypeError, ValueError):
        raise StorageError("The saved species catalogue is invalid. An editor should check atlas/species.json.") from None


def publish_species(store, record, snapshot, expected_sha):
    record = validate_species(record, require_source=True)
    additions = copy.deepcopy(snapshot) + [record]
    merge_species(additions)  # Includes duplicate checks against the bundled atlas.
    body = dict(message=f"Publish atlas species: {record['species_name']}", branch=store.branch,
                content=base64.b64encode(json.dumps(additions, ensure_ascii=False, indent=2).encode()).decode())
    if expected_sha:
        body["sha"] = expected_sha
    response = store.request("PUT", f"/contents/{CATALOG_PATH}", json=body)
    if response.status_code not in (200, 201):
        # Retry after an uncertain timeout: an identical saved catalogue is success.
        current, sha = read_catalog(store)
        if current == additions:
            return current, sha
        raise StorageError("The catalogue changed or could not be saved. Reload the catalogue, then try again; no existing profiles were overwritten.")
    return additions, response.json()["content"]["sha"]
