# Data Model: Intelligent Agent-Based Routing System

## Core Entities

### UserRequest
Represents a natural language query from the user.

**Fields**:
- `id`: str (UUID) - Unique request identifier
- `text`: str - Raw natural language query
- `timestamp`: datetime - When request was received
- `user_id`: str (optional) - User identifier if available
- `conversation_id`: str - Links to conversation history
- `metadata`: dict - Additional context (source, channel, etc.)

**Validation**:
- `text` must be non-empty, max 1000 characters
- `timestamp` must be valid datetime
- `conversation_id` must reference existing conversation

**State Transitions**:
- Created → Analyzing → Analyzed → Executing → Completed
- Created → Analyzing → Failed (on error)
- Any state → Cancelled (user cancellation)

### AnalysisResult
System's interpretation of user intent and required agents.

**Fields**:
- `id`: str (UUID) - Unique analysis identifier
- `request_id`: str - Reference to UserRequest
- `intent`: str - Interpreted user intent
- `confidence`: float - Confidence score (0.0-1.0)
- `required_agents`: List[str] - Agent IDs needed
- `requires_clarification`: bool - Whether ambiguous
- `clarification_options`: List[str] - Options if ambiguous
- `context_used`: dict - Context that influenced analysis
- `execution_plan`: str - Human-readable plan

**Validation**:
- `confidence` must be between 0.0 and 1.0
- `required_agents` must reference registered agents
- If `requires_clarification` is true, `clarification_options` must not be empty

**Relationships**:
- Many-to-one with UserRequest
- One-to-many with Agent (through required_agents)

### Agent
Specialized component handling specific data domains.

**Fields**:
- `id`: str - Unique agent identifier (e.g., "crm", "scheduler")
- `name`: str - Human-friendly name
- `description`: str - What the agent does
- `capabilities`: List[str] - What it can handle
- `data_source`: str - Primary data source (file, API, etc.)
- `status`: str - Current status (available, busy, error)
- `dependencies`: List[str] - Other agents it might need

**Validation**:
- `id` must be unique, lowercase, alphanumeric
- `capabilities` must have at least one capability
- `status` must be one of: available, busy, error, maintenance

**State Transitions**:
- Available → Busy (when processing)
- Busy → Available (when complete)
- Any → Error (on failure)
- Error → Available (on recovery)

### CoordinationPlan
Sequence of agent operations with dependencies.

**Fields**:
- `id`: str (UUID) - Unique plan identifier
- `analysis_id`: str - Reference to AnalysisResult
- `steps`: List[ExecutionStep] - Ordered execution steps
- `status`: str - Current execution status
- `created_at`: datetime - Plan creation time
- `started_at`: datetime (optional) - Execution start time
- `completed_at`: datetime (optional) - Execution end time
- `result`: dict (optional) - Final aggregated result

**Validation**:
- `steps` must have at least one step
- Step dependencies must form a DAG (no cycles)
- `status` must be valid state

**State Transitions**:
- Planned → Executing → Completed
- Planned → Executing → Failed
- Any state → Cancelled

### ExecutionStep
Individual step in coordination plan.

**Fields**:
- `id`: str (UUID) - Unique step identifier
- `agent_id`: str - Agent to execute this step
- `task_description`: str - What the agent should do
- `dependencies`: List[str] - Step IDs that must complete first
- `input_data`: dict - Data to pass to agent
- `output_data`: dict (optional) - Result from agent
- `status`: str - Step execution status
- `error`: str (optional) - Error message if failed

**Validation**:
- `agent_id` must reference existing agent
- `dependencies` must reference existing steps in same plan
- `status` must be valid state

**State Transitions**:
- Pending → Running → Completed
- Pending → Running → Failed
- Pending → Skipped (if dependencies fail)

### Context
Additional information for disambiguation.

**Fields**:
- `conversation_id`: str - Unique conversation identifier
- `messages`: List[Message] - Recent conversation history
- `user_profile`: dict (optional) - User preferences/info
- `session_data`: dict - Current session information
- `timestamp`: datetime - Context snapshot time

**Validation**:
- `messages` limited to last 10 messages
- `timestamp` must be valid datetime

### Message
Single message in conversation history.

**Fields**:
- `id`: str (UUID) - Unique message identifier
- `role`: str - "user" or "assistant"
- `content`: str - Message text
- `timestamp`: datetime - When message was sent

**Validation**:
- `role` must be "user" or "assistant"
- `content` must be non-empty

## Relationships

```
UserRequest 1 ──→ * AnalysisResult
AnalysisResult * ──→ * Agent (through required_agents)
AnalysisResult 1 ──→ 1 CoordinationPlan
CoordinationPlan 1 ──→ * ExecutionStep
ExecutionStep * ──→ 1 Agent
ExecutionStep * ──→ * ExecutionStep (dependencies)
Context 1 ──→ * Message
UserRequest * ──→ 1 Context (through conversation_id)
```

## Data Persistence

### Storage Strategy
- **Requests & Results**: JSON files organized by date
- **Agent Registry**: YAML configuration file
- **Context**: In-memory with file backup
- **Logs**: Structured JSON logs with rotation

### File Structure
```
data/
├── requests/
│   └── 2025-09-14/
│       └── {request_id}.json
├── agents/
│   └── registry.yaml
├── context/
│   └── {conversation_id}.json
└── logs/
    └── routing-decisions.jsonl
```

## Validation Rules Summary

1. All IDs must be valid UUIDs (except agent IDs)
2. Timestamps must be ISO 8601 format
3. Status fields must use defined enums
4. References must point to existing entities
5. Lists must respect size limits (messages: 10, text: 1000 chars)
6. Confidence scores must be normalized (0.0-1.0)
7. Dependencies must not create cycles