from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Iterable
import yaml

from src.models.agent import Agent


class AgentRegistry:
    """Registry that loads agents from a YAML file."""

    def __init__(self, registry_path: Path | str = Path("data/agents/registry.yaml")) -> None:
        self.registry_path = Path(registry_path)
        self._agents: Dict[str, Agent] = {}
        self._load()

    def _load(self) -> None:
        if not self.registry_path.exists():
            return
        with open(self.registry_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or []
        for item in data:
            agent = Agent(**item)
            self._agents[agent.id] = agent

    def list_agents(self) -> List[Agent]:
        return list(self._agents.values())

    def register_agent(self, agent: Agent) -> None:
        self._agents[agent.id] = agent

    def get_agent(self, agent_id: str) -> Agent | None:
        return self._agents.get(agent_id)

    def find_agents_by_capability(self, capability: str) -> List[Agent]:
        return [a for a in self._agents.values() if capability in a.capabilities]
