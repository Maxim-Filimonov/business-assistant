# LLM Configuration Guide

This CrewAI application supports multiple LLM providers. You can easily switch between OpenAI and Ollama (local models).

## Quick Start

### Option 1: Using OpenAI (Default)

1. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

3. Test the configuration:
   ```bash
   python test_config.py
   ```

### Option 2: Using Ollama with Qwen (Local)

1. Install Ollama from https://ollama.ai

2. Pull the Qwen model:
   ```bash
   ollama pull qwen
   # or for Qwen2:
   ollama pull qwen2
   ```

3. Switch to Ollama in `.env`:
   ```
   LLM_PROVIDER=ollama
   ```

4. (Optional) Update the model name in `config.py` if using qwen2:
   ```python
   OLLAMA_MODEL = "qwen2"  # or keep as "qwen"
   ```

5. Test the configuration:
   ```bash
   python test_config.py
   ```

## Configuration Details

### Switching Providers

You can switch providers in three ways:

1. **Environment variable** (recommended):
   - In `.env` file: `LLM_PROVIDER=ollama` or `LLM_PROVIDER=openai`

2. **Direct edit** in `config.py`:
   ```python
   LLM_PROVIDER = "ollama"  # or "openai"
   ```

3. **Runtime override** (for testing):
   ```python
   from config import get_llm
   llm = get_llm(provider="ollama")  # Force specific provider
   ```

### Available Models

**OpenAI:**
- `gpt-4o-mini` (default, fastest and cheapest)
- `gpt-4`
- `gpt-3.5-turbo`

**Ollama:**
- `qwen` (recommended)
- `qwen2`
- `llama2`
- `mistral`
- Any model from https://ollama.ai/library

### Troubleshooting

**OpenAI Issues:**
- "API key not set": Add your key to `.env` file
- "Rate limit": Switch to a different model or use Ollama

**Ollama Issues:**
- "Connection refused": Start Ollama with `ollama serve`
- "Model not found": Pull the model with `ollama pull <model-name>`
- Check available models: `ollama list`

### Testing

Run the test script to verify your configuration:
```bash
python test_config.py
```

This will:
- Check if your chosen provider is configured correctly
- Create a test LLM instance
- Verify agent creation with the LLM
- Show Ollama status and available models