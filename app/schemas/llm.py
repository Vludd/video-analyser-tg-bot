from app.schemas import BaseConfig
from typing import Optional

class SystemPromptElementData(BaseConfig):
    role: str
    content: str

class LLMCompletionData(BaseConfig):
    prompt: str
    system_prompt: Optional[SystemPromptElementData]
