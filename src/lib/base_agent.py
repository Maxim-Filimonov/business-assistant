from __future__ import annotations

from typing import List, Optional, Dict


class BaseAgent:
    """Base class for all agents following the contract spec."""

    def __init__(self, agent_id: str, name: str, description: str, *, version: str = "0.1.0", data_source: Optional[str] = None) -> None:
        self.id = agent_id
        self.name = name
        self.description = description
        self.version = version
        self.data_source = data_source

    # Interface methods
    def get_capabilities(self) -> List[str]:
        raise NotImplementedError

    def can_handle(self, intent: str, context: Dict) -> Dict:
        raise NotImplementedError

    def execute_task(self, task_description: str, input_data: Dict, context: Dict) -> Dict:
        raise NotImplementedError

    def get_dependencies(self) -> List[str]:
        return []

    def get_status(self) -> Dict:
        return {"status": "available", "message": "Ready"}
