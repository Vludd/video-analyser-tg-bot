import torch

from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    BitsAndBytesConfig
)

import logging

from app.config.llm import LLM_DEVICE

logger = logging.getLogger(__name__)

class LLMEngine:
    def __init__(self, model_id: str, system_prompt: str = "") -> None:
        self.system_prompt = system_prompt
        self.context = []
        
        self._load_model(model_id)
        self._load_context(system_prompt)
        
    def _get_device_map(self):
        if LLM_DEVICE == "cpu":
            return {"": "cpu"}

        return "auto"
        
    def _load_model(self, model_id: str = ""):
        logger.info("Initializaion LLM engine...")
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            local_files_only=True,
            quantization_config=BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
            ),
            device_map=self._get_device_map(),
            max_memory={0: "7GiB", "cpu": "30GiB"},
            dtype="auto",
            low_cpu_mem_usage=True,
        )
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        logger.info(
            "LLM device: %s | CUDA available: %s ",
            LLM_DEVICE,
            torch.cuda.is_available(),
        )
        
    def _load_context(self, system_prompt: str) -> None:
        if system_prompt:
            system_prompt_item = {"role": "system", "content": system_prompt}
            self.context.append(system_prompt_item)
    
    def completion(self, prompt: str):
        self.context.append({"role": "user", "content": prompt})

        prompt = self.tokenizer.apply_chat_template(
            self.context,
            tokenize=False,
            add_generation_prompt=True
        )

        input_tokenized = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        input_ids = input_tokenized["input_ids"]
        input_tokens = input_ids.shape[1]
        
        input_len = input_tokens

        with torch.inference_mode():
            output_ids = self.model.generate(
                input_ids=input_ids,
                attention_mask=input_tokenized.get("attention_mask"),
                max_new_tokens=1024,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=getattr(self.tokenizer, "eos_token_id", None),
                use_cache=True,
            )

        reply_ids = output_ids[0, input_len:]
        output_tokens = reply_ids.shape[0]
        
        reply = self.tokenizer.decode(reply_ids, skip_special_tokens=True).strip()
        self.context.append({"role": "assistant", "content": reply})
        
        total_context_tokens = input_tokens + output_tokens
        max_context = self.model.config.max_position_embeddings
        tokens_left = max_context - total_context_tokens
        
        logger.info(
            f"Usage:\n"
            f"  Input: {input_tokens}\n"
            f"  Output: {output_tokens}\n"
            f"  Total: {total_context_tokens}\n"
            f"  Remaining: {tokens_left}\n"
            f"  MaxContext: {max_context}"
        )
        
        torch.cuda.empty_cache()
        
        return {
            "reply": reply,
            "usage": {
                "input": input_tokens,
                "output": output_tokens,
                "total": total_context_tokens,
                "remaining": tokens_left,
                "max": max_context
            }
        }
