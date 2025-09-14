# Claude Code Assistant Context

## Project Overview
CrewAI-based intelligent agent orchestration system that analyzes user intent to coordinate multiple specialized agents without keyword matching.

## Current Feature Branch
`001-intelligent-agent-based` - Implementing intent-based routing system

## Tech Stack
- **Language**: Python 3.11
- **Framework**: CrewAI 0.186.1
- **LLM**: OpenAI API / Ollama
- **Testing**: pytest, pytest-asyncio
- **Dependencies**: LangChain 0.3.27, pydantic

## Project Structure
```
src/
├── models/          # Request, Analysis, Coordination entities
├── services/        # Orchestrator, IntentAnalyzer, AgentRegistry
├── cli/            # Command-line interface
└── lib/            # ContextManager, RoutingLogger

tests/
├── contract/       # API contract tests (TDD)
├── integration/    # Agent coordination tests
└── unit/          # Component tests
```

## Current Implementation Status
- [x] Feature specification complete
- [x] Research and technical decisions made
- [x] Data models designed
- [x] API contracts defined
- [x] Quickstart guide created
- [ ] Task list generation (next: /tasks command)
- [ ] Implementation
- [ ] Testing

## Key Design Decisions
1. **Intent Analysis**: LLM-based with structured prompting
2. **Agent Coordination**: Sequential with context passing via CrewAI
3. **Ambiguity Handling**: Explicit clarification requests
4. **Context Sources**: Conversation history + request metadata
5. **Performance**: 30-second timeout, 2 concurrent requests

## Testing Approach
- TDD: Tests written before implementation
- Contract tests first, then integration, then unit
- Real dependencies (actual LLM calls, file access)
- Performance validation for response times

## Key Files to Know
- `main.py` - Current implementation with keyword routing (to be replaced)
- `agents/` - Existing CRM, Scheduler, Invoice agents
- `specs/001-intelligent-agent-based/` - Feature documentation
- `data/` - Sample data files (clients.md, schedules)

## Common Commands
```bash
# Run the system
python main.py "Your natural language request"

# Run tests
pytest tests/

# Check agent status
python main.py --list-agents

# Continue conversation
python main.py --continue-conversation [id] "Request"
```

## Current Challenges
- Replacing keyword-based routing with intent analysis
- Ensuring proper agent coordination for complex requests
- Handling ambiguous requests gracefully
- Maintaining context across conversations

## Next Steps
1. Run `/tasks` command to generate implementation tasks
2. Implement contract tests (TDD approach)
3. Build orchestrator service
4. Replace existing routing logic
5. Validate with quickstart scenarios

## Recent Changes
- 2025-09-14: Initial feature specification created
- 2025-09-14: Technical research completed
- 2025-09-14: Data models and contracts designed
- 2025-09-14: Implementation plan finalized

## Notes for Claude
- Follow TDD strictly - tests must fail before implementation
- Use CrewAI's built-in features for agent coordination
- Keep orchestration logic separate from individual agents
- Log all routing decisions for debugging
- Preserve existing agent functionality