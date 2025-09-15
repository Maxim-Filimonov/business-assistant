from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Agent:
    """Represents a registered agent."""

    id: str
    name: str
    description: str
    capabilities: List[str]
    status: str = "available"
    data_source: Optional[str] = None
    version: str = "0.1.0"
