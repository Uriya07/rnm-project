import requests
import csv

URL = "https://rickandmortyapi.com/api/character"

def fetch_all_characters():
    """Fetch all characters from all pages."""
    all_results = []
    url = URL
    while url:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        all_results.extend(data.get("results", []))
        url = data.get("info", {}).get("next")
    return all_results

def filter_human_alive_earth(characters):
    """Keep only Human + Alive + origin contains 'Earth'."""
    filtered = []
    for c in characters:
        species = (c.get("species") or "").strip().lower()
        status = (c.get("status") or "").strip().lower()
        origin_name = ((c.get("origin") or {}).get("name") or "").strip().lower()
        if species == "human" and status == "alive" and ("earth" in origin_name):
            filtered.append({
                "name": c.get("name"),
                "location": (c.get("location") or {}).get("name"),
                "image": c.get("image"),
            })
    return filtered

def write_csv(rows, path):
    """Write rows to a CSV file with headers: Name, Location, Image."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Name", "Location", "Image"])
        for r in rows:
            w.writerow([r["name"], r["location"], r["image"]])

if __name__ == "__main__":
    all_chars = fetch_all_characters()
    result = filter_human_alive_earth(all_chars)
    print(f"Found {len(result)} characters. Writing to out.csv ...")
    write_csv(result, "out.csv")
    print("Done. Open out.csv to verify the first rows.")



