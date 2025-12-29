import json
from pathlib import Path

def parse_json(path: Path) -> dict:
    raw_data = ""
    with open(path, "r") as f:
        raw_data = json.load(f)
    
    return raw_data
