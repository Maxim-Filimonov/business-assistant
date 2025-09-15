from src.services.agent_registry import AgentRegistry


def test_agent_registry_lists_agents_and_finds_by_capability():
    registry = AgentRegistry()
    agents = registry.list_agents()
    assert any(a.id == "crm" for a in agents)
    scheduling_agents = registry.find_agents_by_capability("check_schedule")
    assert any(a.id == "scheduler" for a in scheduling_agents)
