#!/usr/bin/env python
"""
Test script to verify LLM configuration
"""

import sys
from config import get_llm, LLM_PROVIDER, OPENAI_API_KEY

def test_config():
    print("\n" + "="*50)
    print("TESTING LLM CONFIGURATION")
    print("="*50)

    print(f"\nCurrent provider: {LLM_PROVIDER}")

    if LLM_PROVIDER == "openai":
        if not OPENAI_API_KEY:
            print("\n❌ OpenAI API key not set!")
            print("\nTo use OpenAI, either:")
            print("1. Create a .env file with: OPENAI_API_KEY=your-key-here")
            print("2. Or set environment variable: export OPENAI_API_KEY='your-key-here'")
            print("\nTo switch to Ollama (when Qwen is ready):")
            print("1. Edit config.py and change LLM_PROVIDER to 'ollama'")
            print("2. Or add to .env file: LLM_PROVIDER=ollama")
            return False

    try:
        llm = get_llm()
        print(f"✅ LLM instance created successfully: {type(llm).__name__}")

        # Try to import and test agents
        from agents.crm_agent import crm_agent
        agent = crm_agent()
        print(f"✅ CRM Agent created successfully with LLM")

        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def test_ollama_availability():
    print("\n" + "-"*50)
    print("CHECKING OLLAMA STATUS")
    print("-"*50)

    try:
        import subprocess
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama is installed")
            models = result.stdout.strip().split('\n')[1:]  # Skip header
            if models and models[0]:
                print(f"Available models: {models}")
            else:
                print("⚠️  No models installed yet")
                print("To install Qwen: ollama pull qwen")
        else:
            print("❌ Ollama command failed")
    except FileNotFoundError:
        print("❌ Ollama not found. Install from: https://ollama.ai")

if __name__ == "__main__":
    success = test_config()
    test_ollama_availability()

    print("\n" + "="*50)
    if success:
        print("✅ Configuration test PASSED")
    else:
        print("❌ Configuration test FAILED")
    print("="*50)

    sys.exit(0 if success else 1)
