"""
Configuration management for the Fake News Detector app
"""


import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv


@dataclass
class Config:
    """Application configuration"""

    def __init__(self):
        # Load environment variables
        load_dotenv()

        # LLM API Keys
        self.openai_api_key: Optional[str] = os.getenv('OPENAI_API_KEY')

        # LLM Analysis configuration
        self.model_name: str = os.getenv('MODEL_NAME', "gpt-5-nano")
        self.max_tokens: int = int(os.getenv('MAX_TOKENS', '1000'))
        self.temperature: float = float(os.getenv('TEMPERATURE', '0.3'))

        # Google search API key and Id
        self.google_api_key: Optional[str] = os.getenv('GOOGLE_API_KEY')
        self.google_cse_id: Optional[str] = os.getenv('GOOGLE_CSE_ID')

        # Search configuration
        self.max_search_results: int = int(os.getenv('MAX_SEARCH_RESULTS', '5'))
        self.search_timeout: int = int(os.getenv('SEARCH_TIMEOUT', '10'))

    def validate(self) -> bool:
        """Validate required configuration"""
        if not self.openai_api_key:
            return False
        return True
