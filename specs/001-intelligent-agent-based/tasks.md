# Tasks: Intelligent Agent-Based Routing System

**Input**: Design documents from `/specs/001-intelligent-agent-based/`
**Prerequisites**: plan.md ✓, research.md ✓, data-model.md ✓, contracts/ ✓

## Execution Flow (main)
```
1. Load plan.md from feature directory ✓
2. Load optional design documents ✓
3. Generate tasks by category ✓
4. Apply task rules ✓
5. Number tasks sequentially ✓
6. Generate dependency graph ✓
7. Create parallel execution examples ✓
8. Validate task completeness ✓
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Single project**: `src/`, `tests/` at repository root
- Tech stack: Python 3.11, CrewAI 0.186.1, pytest
- Type: CLI tool (no web endpoints)

## Phase 3.1: Setup

- [ ] T001 Create project structure per implementation plan - directories src/{models,services,cli,lib}, tests/{contract,integration,unit}
- [ ] T002 Update requirements.txt with CrewAI 0.186.1, LangChain 0.3.27, pytest, pytest-asyncio dependencies
- [ ] T003 [P] Configure pytest.ini and .env.example with OpenAI API key placeholder
- [ ] T004 [P] Create logging configuration in src/config.py with JSON formatter and rotation
- [ ] T005 [P] Initialize agent registry YAML at data/agents/registry.yaml with CRM, scheduler, invoicer entries

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3

### Contract Tests (Agent Interfaces)
- [ ] T006 [P] Create tests/contract/test_agent_interface.py validating all agents implement standard interface
- [ ] T007 [P] Create tests/contract/test_orchestrator_contract.py for orchestrator's analyze/execute/clarify methods
- [ ] T008 [P] Create tests/contract/test_intent_analyzer_contract.py for intent analysis interface
- [ ] T009 [P] Create tests/contract/test_agent_registry_contract.py for agent discovery interface
- [ ] T010 [P] Create tests/contract/test_context_manager_contract.py for context aggregation interface

### Integration Tests
- [ ] T011 [P] Create tests/integration/test_intent_recognition.py from quickstart Test 1 scenarios
- [ ] T012 [P] Create tests/integration/test_context_awareness.py from quickstart Test 2 scenarios
- [ ] T013 [P] Create tests/integration/test_agent_coordination.py from quickstart Test 3 scenarios
- [ ] T014 [P] Create tests/integration/test_morning_report.py for Scenario 1: schedule + CRM coordination
- [ ] T015 [P] Create tests/integration/test_billing_query.py for Scenario 2: schedule + invoice coordination
- [ ] T016 [P] Create tests/integration/test_workload_analysis.py for Scenario 3: single agent routing

## Phase 3.3: Core Implementation

### Models (Entities from data-model.md)
- [ ] T017 [P] Implement src/models/request.py with UserRequest class and state transitions
- [ ] T018 [P] Implement src/models/analysis.py with AnalysisResult class and validation
- [ ] T019 [P] Implement src/models/agent.py with Agent class and capability management
- [ ] T020 [P] Implement src/models/coordination.py with CoordinationPlan and ExecutionStep classes
- [ ] T021 [P] Implement src/models/context.py with Context and Message classes

### Core Services
- [ ] T022 Implement src/services/intent_analyzer.py with LLM-based analysis using structured prompting
- [ ] T023 Implement src/services/agent_registry.py with agent discovery and capability matching
- [ ] T024 Implement src/services/orchestrator.py with main orchestration logic combining analyzer and registry
- [ ] T025 [P] Implement src/lib/context_manager.py for conversation history and metadata aggregation
- [ ] T026 [P] Implement src/lib/routing_logger.py for structured JSON logging of routing decisions

### Agent Base Class
- [ ] T027 [P] Implement src/lib/base_agent.py with standard interface from agent-interface.yaml
- [ ] T028 Update existing agents (CRM, Scheduler, Invoice) to inherit from BaseAgent

### CLI Interface
- [ ] T029 Implement src/cli/orchestrate.py with main command entry point
- [ ] T030 Add --list-agents command to show available agents and capabilities
- [ ] T031 Add --continue-conversation flag for context preservation
- [ ] T032 Add --format json/text flag for output formatting
- [ ] T033 Add --verbose flag for detailed routing decisions

## Phase 3.4: Integration & Orchestration

- [ ] T034 Integrate orchestrator with existing CrewAI agents (CRM, Scheduler, Invoice)
- [ ] T035 Implement request processing pipeline in main.py using orchestrator
- [ ] T036 Add async request handling for 2 concurrent requests support
- [ ] T037 Implement timeout handling (30 seconds) with partial results on timeout
- [ ] T038 Add caching layer for repeated analysis optimization
- [ ] T039 Implement conversation persistence to maintain context across sessions

## Phase 3.5: Polish & Documentation

- [ ] T040 [P] Create unit tests for intent_analyzer.py with mocked LLM responses
- [ ] T041 [P] Create unit tests for agent_registry.py with test agents
- [ ] T042 [P] Create unit tests for context_manager.py with sample conversations
- [ ] T043 [P] Add performance tests validating 30-second response time requirement
- [ ] T044 [P] Create llms.txt documentation for each library (orchestrator, agent_registry, context_manager)
- [ ] T045 Remove old keyword-based routing from main.py
- [ ] T046 Run full test suite and ensure all tests pass (contract → integration → unit)
- [ ] T047 Execute quickstart.md scenarios for end-to-end validation
- [ ] T048 Update README.md with new intelligent routing capabilities

## Parallel Execution Examples

### After T005 completes, run in parallel:
```bash
# Terminal 1-5 (Contract Tests for Interfaces)
python -m pytest tests/contract/test_agent_interface.py         # T006
python -m pytest tests/contract/test_orchestrator_contract.py   # T007
python -m pytest tests/contract/test_intent_analyzer_contract.py # T008
python -m pytest tests/contract/test_agent_registry_contract.py # T009
python -m pytest tests/contract/test_context_manager_contract.py # T010
```

### After T010 completes, run in parallel:
```bash
# Terminal 1-6 (Integration Tests)
python -m pytest tests/integration/test_intent_recognition.py    # T011
python -m pytest tests/integration/test_context_awareness.py     # T012
python -m pytest tests/integration/test_agent_coordination.py    # T013
python -m pytest tests/integration/test_morning_report.py        # T014
python -m pytest tests/integration/test_billing_query.py         # T015
python -m pytest tests/integration/test_workload_analysis.py     # T016
```

### After T016 completes, run in parallel:
```bash
# Terminal 1-5 (Models)
python src/models/request.py      # T017
python src/models/analysis.py     # T018
python src/models/agent.py        # T019
python src/models/coordination.py # T020
python src/models/context.py      # T021
```

## Task Dependencies

```
Setup (T001-T005)
    ↓
Contract Tests (T006-T010) [PARALLEL] - Test interfaces, not HTTP
    ↓
Integration Tests (T011-T016) [PARALLEL]
    ↓
Models (T017-T021) [PARALLEL]
    ↓
Services (T022-T026) [MIXED]
    ↓
Agent Base (T027-T028) 
    ↓
CLI (T029-T033) [SEQUENTIAL - same file]
    ↓
Integration (T034-T039) [SEQUENTIAL - system integration]
    ↓
Polish (T040-T048) [MOSTLY PARALLEL]
```

## Validation Checklist

- [x] All agent interfaces have tests (T006-T010)
- [x] All entities have models (T017-T021)
- [x] CLI commands implemented (T029-T033)
- [x] All user scenarios covered (T011-T016)
- [x] TDD order maintained (tests before implementation)
- [x] Parallel tasks properly marked
- [x] Dependencies clearly defined
- [x] No unnecessary HTTP endpoints (CLI tool only)

## Notes for Implementation

1. **CRITICAL**: Complete ALL tests (T006-T016) before ANY implementation (T017+)
2. Tests MUST fail initially (Red phase of Red-Green-Refactor)
3. This is a CLI tool - no HTTP server, no REST endpoints
4. Orchestrator methods are Python methods, not HTTP endpoints
5. Use actual LLM calls in integration tests, mock only in unit tests
6. Each git commit should show test → implementation pattern
7. Performance target: 30 seconds max for analysis
8. Support 2 concurrent requests using asyncio

## Estimated Effort

- Setup: 1 hour
- Contract Tests: 2 hours (simpler without HTTP)
- Integration Tests: 3-4 hours
- Models: 2 hours
- Services: 4-5 hours
- Agent Base: 1-2 hours
- CLI: 2-3 hours
- Integration: 3-4 hours
- Polish: 3-4 hours

**Total Estimate**: 21-30 hours