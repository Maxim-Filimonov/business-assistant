from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class ExecutionStep:
    agent_id: str
    action: str
    input_data: Dict = field(default_factory=dict)


@dataclass
class CoordinationPlan:
    steps: List[ExecutionStep] = field(default_factory=list)
