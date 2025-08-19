import re
import json

def validate_amount(value):
    return bool(re.match(r'^\d+(\.\d{1,2})?$', str(value)))

def compute_overall_confidence(fields):
    if not fields:
        return 0.0
    return sum(f.get("confidence", 0) for f in fields) / len(fields)

def validate_output(raw_json: str):
    try:
        data = json.loads(raw_json)
        for f in data["fields"]:
            if "amount" in f["name"].lower() and not validate_amount(f["value"]):
                f["confidence"] *= 0.7
        data["overall_confidence"] = compute_overall_confidence(data["fields"])
        return data
    except Exception as e:
        return {"error": str(e), "raw": raw_json}
