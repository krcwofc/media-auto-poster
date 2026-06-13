import json
from pathlib import Path

CONTENT_DIR = Path("content")

items = []

for source_dir in CONTENT_DIR.iterdir():

    if not source_dir.is_dir():
        continue

    source = source_dir.name.lower()

    for file in source_dir.rglob("*"):

        if not file.is_file():
            continue

        ext = file.suffix.lower()

        if ext not in [
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
            ".gif",
            ".mp4",
            ".mov"
        ]:
            continue

        try:
            year = int(file.name[:4])
        except:
            year = 0

        items.append({
            "file": str(file).replace("\\", "/"),
            "source": source,
            "year": year
        })

with open("index.json", "w", encoding="utf-8") as f:
    json.dump(items, f, indent=2)

print(f"Indexed {len(items)} items")
