# Quickstart: Intelligent Agent-Based Routing System

## Overview
This system intelligently routes user requests to appropriate agents without relying on keyword matching. It understands intent, context, and automatically coordinates multiple agents when needed.

## Prerequisites
- Python 3.11+
- OpenAI API key or Ollama installed
- CrewAI framework

## Installation

```bash
# Clone repository
git clone <repository>
cd crewai_app

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Basic Usage

### 1. Simple Request (Single Agent)

```bash
# Ask about clients
python main.py "Show me all clients"

# Expected behavior:
# - System analyzes intent (listing clients)
# - Routes to CRM agent only
# - Returns client list
```

### 2. Complex Request (Multiple Agents)

```bash
# Cross-reference request
python main.py "Who are the parents of Dr. Johnson's morning appointments?"

# Expected behavior:
# - System identifies need for schedule data (morning appointments)
# - System identifies need for CRM data (parent information)
# - Coordinates: Scheduler → CRM in sequence
# - Returns parent names
```

### 3. Ambiguous Request

```bash
# Ambiguous intent
python main.py "List everyone"

# Expected behavior:
# - System detects ambiguity
# - Asks for clarification:
#   "Do you mean: 1) List all clients, 2) List all appointments, 3) List all staff?"
# - Processes based on selection
```

## Testing the System

### Test 1: Intent Recognition
```python
# test_intent.py
from src.services.orchestrator import Orchestrator

orch = Orchestrator()

# Test various phrasings
requests = [
    "Show me today's schedule",  # Should identify scheduler need
    "Contact info for Sarah",    # Should identify CRM need
    "Morning sessions overview",  # Should identify scheduler need
]

for req in requests:
    result = orch.analyze_request(req)
    print(f"Request: {req}")
    print(f"Intent: {result.intent}")
    print(f"Agents: {result.required_agents}")
    print("---")
```

### Test 2: Context Awareness
```python
# test_context.py
from src.services.orchestrator import Orchestrator
from src.models.context import Context

orch = Orchestrator()

# Create context with history
context = Context(conversation_id="test-123")
context.add_message("user", "I'm interested in Dr. Johnson's schedule")
context.add_message("assistant", "Dr. Johnson has 6 clients this week")

# Ambiguous request that should use context
result = orch.analyze_request("Who are their parents?", context)

# Should understand "their" refers to Dr. Johnson's clients
assert "scheduler" in result.required_agents
assert "crm" in result.required_agents
```

### Test 3: Agent Coordination
```python
# test_coordination.py
from src.services.orchestrator import Orchestrator

orch = Orchestrator()

# Request requiring coordination
request = "Email addresses of this week's group therapy participants"

# Analyze
analysis = orch.analyze_request(request)

# Execute
result = orch.execute_plan(analysis.id)

# Verify coordination happened
assert len(result.steps_executed) > 1
assert result.steps_executed[0].agent_id == "scheduler"
assert result.steps_executed[1].agent_id == "crm"
```

## Configuration

### Agent Registry (`data/agents/registry.yaml`)
```yaml
agents:
  - id: crm
    name: CRM Agent
    description: Manages client information
    capabilities:
      - search_clients
      - get_client_details
      - get_parent_information
    data_source: data/clients.md

  - id: scheduler
    name: Scheduler Agent
    description: Manages appointments and schedules
    capabilities:
      - get_schedule
      - find_appointments
      - check_availability
    data_source: data/sample_schedule.pdf

  - id: invoicer
    name: Invoice Agent
    description: Handles billing and invoices
    capabilities:
      - generate_invoice
      - calculate_costs
      - payment_status
    data_source: data/pricing.md
```

### Logging Configuration
```python
# config.py
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': 'json',
    'file': 'data/logs/routing-decisions.jsonl',
    'max_size': '10MB',
    'retention': '7 days'
}
```

## Common Scenarios

### Scenario 1: Morning Report
```bash
python main.py "Give me a summary of this morning's appointments with client contact info"

# System will:
# 1. Identify time-based schedule query
# 2. Identify need for contact information
# 3. Coordinate scheduler → CRM
# 4. Return formatted report
```

### Scenario 2: Billing Query
```bash
python main.py "Generate invoices for completed sessions this week"

# System will:
# 1. Identify billing intent
# 2. Identify time constraint
# 3. Coordinate scheduler → invoicer
# 4. Generate invoices
```

### Scenario 3: Workload Analysis
```bash
python main.py "Which specialist has the heaviest workload?"

# System will:
# 1. Identify analytical query
# 2. Route to scheduler only
# 3. Analyze appointment distribution
# 4. Return workload summary
```

## Troubleshooting

### Issue: "Cannot determine intent"
**Solution**: The request is too vague. System will ask for clarification.

### Issue: "Agent not available"
**Solution**: Check agent status with:
```bash
python main.py --list-agents
```

### Issue: "Timeout exceeded"
**Solution**: Complex requests may take time. Increase timeout in config:
```python
ANALYSIS_TIMEOUT = 30  # seconds
```

### Issue: "Context lost between requests"
**Solution**: Ensure conversation_id is consistent:
```bash
python main.py --continue-conversation [conversation_id] "Your request"
```

## Performance Validation

Run the performance test suite:
```bash
pytest tests/performance/test_response_time.py

# Should verify:
# - Analysis completes within 30 seconds
# - System handles 2 concurrent requests
# - Context retrieval is under 1 second
```

## Next Steps

1. **Extend agent capabilities**: Add more specialized agents
2. **Improve context**: Add user profiles for better personalization
3. **Add learning**: Track successful routings to improve future analysis
4. **Scale horizontally**: Distribute agents across services

## Support

- Check logs at `data/logs/routing-decisions.jsonl` for debugging
- Run `python main.py --help` for all CLI options
- Import `from src.services.orchestrator import Orchestrator` for programmatic usage