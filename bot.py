import json
import random
import os
import requests

webhook = os.environ["DISCORD_WEBHOOK"]

index = json.load(open("index.json"))
state = json.load(open("state.json"))

seen = set(state.get("seen", []))

counts = state.get("source_counts", {
    "kathryn": 0,
    "james": 0,
    "kathreid": 0
})

available = [x for x in index if x["file"] not in seen]

if not available:
    available = index
    seen = set()
    counts = {"kathryn": 0, "james": 0, "kathreid": 0}

def score(item):
    source = item["source"]
    return (1 / (1 + counts.get(source, 0))) * random.uniform(0.85, 1.15)

weighted = sorted(available, key=score, reverse=True)

pool = weighted[:5] if len(weighted) >= 5 else weighted
item = random.choice(pool)

captions = json.load(open("captions.json"))
caption = random.choice(captions).format(year=item["year"])

with open(item["file"], "rb") as f:
    requests.post(
        webhook,
        data={"content": caption},
        files={"file": f}
    )

seen.add(item["file"])
counts[item["source"]] = counts.get(item["source"], 0) + 1

state["seen"] = list(seen)
state["source_counts"] = counts

with open("state.json", "w") as f:
    json.dump(state, f, indent=2)

print("Posted:", item["file"])
