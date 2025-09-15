from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict
import uuid


@dataclass
class AnalysisResult:
    """Result of intent analysis."""

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    request_id: uuid.UUID = field(default_factory=uuid.uuid4)
    intent: str = ""
    confidence: float = 0.0
    required_agents: List[str] = field(default_factory=list)
    requires_clarification: bool = False
    clarification_options: List[str] = field(default_factory=list)
    context_used: Dict = field(default_factory=dict)
    execution_plan: str = ""
