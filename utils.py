import json
import os

def save_json(data, filename="output.json"):
    os.makedirs("outputs", exist_ok=True)
    path = os.path.join("outputs", filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    return path
