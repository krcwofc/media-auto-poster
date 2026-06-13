import os
import json

CONTENT_DIR = "content"

allowed_ext = (".jpg", ".jpeg", ".png", ".mp4", ".mov")

index = []

for source in os.listdir(CONTENT_DIR):
    source_path = os.path.join(CONTENT_DIR, source)

    if not os.path.isdir(source_path):
        continue

    for year in os.listdir(source_path):
        year_path = os.path.join(source_path, year)

        if not os.path.isdir(year_path):
            continue

        for file in os.listdir(year_path):
            if not file.lower().endswith(allowed_ext):
                continue

            full_path = os.path.join(year_path, file)

            file_type = "video" if file.lower().endswith((".mp4", ".mov")) else "image"

            index.append({
                "file": full_path,
                "year": int(year),
                "source": source,
                "type": file_type
            })

with open("index.json", "w") as f:
    json.dump(index, f, indent=2)

print(f"Generated {len(index)} entries")
