import json
from pathlib import Path


def parse_json(path: Path) -> dict:
    raw_data = ""
    with open(path, "r") as f:
        raw_data = json.load(f)
    
    return raw_data

def load_prompt(path: Path) -> str:
    prompt = ""
    with open(path, "r") as f:
        prompt = f.read()
    
    return prompt

def parse_llm_response(raw_text: str) -> dict:
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        raise ValueError("LLM returned invalid JSON")
