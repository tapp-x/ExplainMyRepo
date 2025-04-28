from langchain_core.language_models import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from typing import Optional, List
from pydantic import Field
import requests
import json
import os


from dotenv import load_dotenv

load_dotenv()

LLM_URL = os.getenv("LLM_URL")

class CustomLLM(LLM):
	url: str = Field(default=LLM_URL)
	model: str = Field(default="mistral")

	def _call(self, prompt: str, stop: Optional[List[str]] = None, run_manager: Optional[CallbackManagerForLLMRun] = None) -> str:
		payload = {
			"model": self.model,
			"prompt": prompt,
			"stream": False
		}

		try:
			response = requests.post(self.url, json=payload)
			return json.loads(response.content)['response']
		except requests.RequestException as e:
			print(f"Erreur : {e}")

	@property
	def _llm_type(self) -> str:
		return "custom-remote-llm"
