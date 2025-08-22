from fastapi import FastAPI
import requests
import csv
from io import StringIO
from fastapi.responses import Response

app = FastAPI(title="Rick & Morty Filter API")

API_URL = "https://rickandmortyapi.com/api/character"


def fetch_all_characters():
    """Fetch ALL characters by following pagination until 'next' is None."""
    all_results = []
    url = API_URL
    while url:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        all_results.extend(data.get("results", []))
        url = data.get("info", {}).get("next")  # None when no more pages
    return all_results


def filter_human_alive_earth(characters):
    """Keep only Human + Alive + origin contains 'Earth' (case-insensitive)."""
    filtered = []
    for c in characters:
        species = (c.get("species") or "").strip().lower()
        status = (c.get("status") or "").strip().lower()
        origin_name = ((c.get("origin") or {}).get("name") or "").strip().lower()
        if species == "human" and status == "alive" and "earth" in origin_name:
            filtered.append(
                {
                    "name": c.get("name"),
                    "location": (c.get("location") or {}).get("name"),
                    "image": c.get("image"),
                }
            )
    return filtered


@app.get("/")
def root():
    """Simple landing message for the root path."""
    return {"message": "Rick & Morty Filter API. Try /health, /characters, or /csv"}


@app.get("/health")
def health():
    """Health endpoint for readiness/liveness checks."""
    return {"ok": True}


@app.get("/characters")
def get_characters():
    """Return filtered characters as JSON."""
    all_chars = fetch_all_characters()
    return filter_human_alive_earth(all_chars)


@app.get("/csv")
def get_csv():
    """Return filtered characters as CSV (download in browser)."""
    # 1) Fetch + filter
    all_chars = fetch_all_characters()
    rows = filter_human_alive_earth(all_chars)

    # 2) Build CSV in-memory
    buff = StringIO()
    writer = csv.writer(buff)
    writer.writerow(["Name", "Location", "Image"])
    for r in rows:
        writer.writerow([r["name"], r["location"], r["image"]])

    # 3) Return as downloadable CSV
    csv_bytes = buff.getvalue().encode("utf-8")
    return Response(
        content=csv_bytes,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=out.csv"},
    )


