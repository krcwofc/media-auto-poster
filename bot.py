import json
import random
import os
import requests

from datetime import datetime
from zoneinfo import ZoneInfo

# =====================================
# CONFIG
# =====================================

webhook = os.environ["DISCORD_WEBHOOK"]

# =====================================
# MANILA TIME
# =====================================

manila_hour = datetime.now(
    ZoneInfo("Asia/Manila")
).hour

# =====================================
# BROADCAST BLOCKS
# =====================================

if 6 <= manila_hour < 12:
    block_name = "🌅 Morning Archive"

    weights = {
        "kathryn": 40,
        "james": 40,
        "kathreid": 20
    }

elif 12 <= manila_hour < 18:
    block_name = "☀️ Daytime Broadcast"

    weights = {
        "kathryn": 35,
        "james": 35,
        "kathreid": 30
    }

else:
    block_name = "🌙 Prime Time Archive"

    weights = {
        "kathryn": 20,
        "james": 20,
        "kathreid": 60
    }

# =====================================
# LOAD FILES
# =====================================

with open("index.json", "r", encoding="utf-8") as f:
    index = json.load(f)

with open("state.json", "r", encoding="utf-8") as f:
    state = json.load(f)

with open("captions.json", "r", encoding="utf-8") as f:
    captions = json.load(f)

seen = set(state.get("seen", []))

# =====================================
# PICK SOURCE BY TIME BLOCK
# =====================================

preferred_source = random.choices(
    population=list(weights.keys()),
    weights=list(weights.values()),
    k=1
)[0]

# =====================================
# FIND AVAILABLE CONTENT
# =====================================

available = [
    item for item in index
    if item["file"] not in seen
    and item["source"] == preferred_source
]

# fallback if source exhausted

if not available:
    available = [
        item for item in index
        if item["file"] not in seen
    ]

# full reset after archive completed

if not available:
    seen = set()
    available = index

# =====================================
# SELECT ITEM
# =====================================

item = random.choice(available)

# =====================================
# CAPTION
# =====================================

caption_template = random.choice(captions)

caption = (
    f"{block_name}\n\n"
    + caption_template.format(year=item["year"])
)

# =====================================
# POST TO DISCORD
# =====================================

with open(item["file"], "rb") as f:
    response = requests.post(
        webhook,
        data={"content": caption},
        files={"file": f}
    )

response.raise_for_status()

# =====================================
# UPDATE STATE
# =====================================

seen.add(item["file"])

state["seen"] = list(seen)

with open("state.json", "w", encoding="utf-8") as f:
    json.dump(state, f, indent=2)

print(f"Posted: {item['file']}")
print(f"Block: {block_name}")
print(f"Source: {preferred_source}")
