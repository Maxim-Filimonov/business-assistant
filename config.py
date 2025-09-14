"""
Configuration for CrewAI with support for multiple LLM providers
"""

import os
from typing import Literal, Optional
from pathlib import Path

# Load environment variables from .env file if it exists
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value

# LLM Provider selection - change this to switch between providers
LLM_PROVIDER: Literal["openai", "ollama"] = os.getenv("LLM_PROVIDER", "openai")  # Change to "ollama" when ready

# OpenAI configuration
OPENAI_MODEL = "gpt-4o-mini"  # or "gpt-4", "gpt-3.5-turbo", etc.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # Set via environment variable

# Ollama configuration
OLLAMA_MODEL = "qwen"  # or "qwen2", "llama2", etc.
OLLAMA_BASE_URL = "http://localhost:11434"

def get_llm(provider: Optional[str] = None):
    """
    Returns the configured LLM instance for CrewAI agents

    Args:
        provider: Override the default provider ("openai" or "ollama")
    """
    active_provider = provider or LLM_PROVIDER

    if active_provider == "ollama":
        from langchain_community.llms import Ollama
        return Ollama(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=0.7,
            num_predict=2048,
            top_p=0.9,
            top_k=40,
        )
    elif active_provider == "openai":
        from langchain_openai import ChatOpenAI
        if not OPENAI_API_KEY:
            raise ValueError(
                "OpenAI API key not found. Please set OPENAI_API_KEY environment variable.\n"
                "Example: export OPENAI_API_KEY='your-api-key-here'"
            )
        return ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=0.7,
            api_key=OPENAI_API_KEY,
            max_tokens=2048,
        )
    else:
        raise ValueError(f"Unknown LLM provider: {active_provider}")

# Print current configuration on import
print(f"🤖 LLM Provider: {LLM_PROVIDER}")
if LLM_PROVIDER == "openai":
    print(f"   Model: {OPENAI_MODEL}")
    print(f"   API Key: {'✓ Set' if OPENAI_API_KEY else '✗ Not set'}")
elif LLM_PROVIDER == "ollama":
    print(f"   Model: {OLLAMA_MODEL}")
    print(f"   URL: {OLLAMA_BASE_URL}")
