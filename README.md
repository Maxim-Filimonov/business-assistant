# CrewAI Business Automation Assistant

An intelligent, AI-powered business assistant that understands natural language and can handle any business request creatively - not limited to pre-programmed commands.

## 🚀 Quick Start

```bash
# Set up your OpenAI API key (or configure for Ollama)
export OPENAI_API_KEY='your-api-key-here'

# Run the chat interface
python main.py

# Or with specific files
python main.py --schedule-pdf data/schedule.pdf
```

## 🧠 What Makes This Special?

Unlike traditional chatbots with fixed commands, this system:
- **Understands Intent**: AI analyzes what you're trying to accomplish
- **Thinks Creatively**: Finds ways to fulfill requests we never explicitly programmed
- **Collaborates**: Multiple AI agents work together to solve complex problems
- **Learns Context**: Remembers conversation history for better responses

## 💬 Example Requests

Ask anything! The AI will figure out how to help:

```
💭 "Find all clients whose parents have Gmail addresses"
💭 "Who hasn't been scheduled in the last month?"
💭 "Compare this week's workload to last week"
💭 "Which specialist is busiest?"
💭 "Create a revenue report by specialist"
💭 "Find patterns in our appointment scheduling"
```

## 🏗️ Architecture

```
Your Natural Language Request
           ↓
    Meta Agent (Orchestrator)
           ↓
    Understands & Plans
           ↓
Coordinates Specialized Agents:
  • CRM Agent (Client Management)
  • Scheduler Agent (Time Management)
  • Invoice Agent (Financial Management)
           ↓
    Creative Solution
```

## 📁 Project Structure

```
crewai_app/
├── main.py              # Main chat interface
├── config.py            # LLM configuration (OpenAI/Ollama)
├── agents/              # Specialized AI agents
│   ├── crm_agent.py
│   ├── scheduler_agent.py
│   ├── invoice_agent.py
│   └── dispatcher_agent.py
├── tasks/               # Dynamic task creation
│   └── dynamic_tasks.py
├── tools/               # Agent tools
│   ├── markdown_tools.py
│   ├── pdf_tools.py
│   └── invoice_tools.py
├── data/                # Your business data
│   ├── clients.md
│   ├── pricing.md
│   └── schedule.pdf
└── templates/           # Document templates
    └── invoice_template.md
```

## ⚙️ Configuration

### Using OpenAI (Default)
1. Create `.env` file:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

### Using Ollama (Local)
1. Install Ollama and pull a model:
   ```bash
   ollama pull qwen
   ```
2. Update `.env`:
   ```
   LLM_PROVIDER=ollama
   ```

See [README_LLM_CONFIG.md](README_LLM_CONFIG.md) for detailed configuration options.

## 🎯 Agent Capabilities

### CRM Agent
- Manages all client information
- Finds relationships and patterns
- Creates client reports
- Handles any client-related query

### Scheduler Agent  
- Extracts schedules from PDFs
- Analyzes appointment patterns
- Finds conflicts and availability
- Handles any time-related query

### Invoice Agent
- Generates invoices dynamically
- Calculates costs and revenue
- Creates financial reports
- Handles any billing-related query

### Meta Agent (Orchestrator)
- Understands your intent
- Plans multi-step solutions
- Coordinates other agents
- Thinks creatively to solve new problems

## 🔧 Installation

```bash
# Clone the repository
git clone <your-repo>
cd crewai_app

# Install dependencies with uv
uv pip install -r requirements.txt

# Configure your LLM (see Configuration above)

# Run the chat
python main.py
```

## 📚 Documentation

- [LLM Configuration Guide](README_LLM_CONFIG.md) - Set up OpenAI or Ollama
- [Flexible Chat Details](README_FLEXIBLE_CHAT.md) - How the AI understands any request

## 💡 Tips

1. **Be Natural**: Just describe what you want in plain English
2. **Be Creative**: Ask for things that aren't in any manual
3. **Provide Context**: More details help the AI understand better
4. **Iterate**: If the first response isn't perfect, clarify your need

## 🤝 Contributing

The beauty of this system is that it can adapt to new use cases without code changes. However, you can:
- Add new tools for agents to use
- Add new data sources
- Improve agent prompts for better understanding
- Share creative use cases

## 📜 License

[Your License Here]