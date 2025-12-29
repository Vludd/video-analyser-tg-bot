from pathlib import Path
from app.core.llm_engine import LLMEngine
from app.utils.data_parser import load_prompt

from app.config.llm import LLM_NAME

path = Path(__file__).parent / "data" / "prompt.md"
    
llm_prompt = load_prompt(path)
llm_engine = LLMEngine(model_id=LLM_NAME, system_prompt=llm_prompt)
