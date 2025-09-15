from src.services.orchestrator import Orchestrator
from src.services.intent_analyzer import IntentAnalyzer
from src.services.agent_registry import AgentRegistry
from src.lib.context_manager import ContextManager


def test_orchestrator_analyze_and_list_agents():
    registry = AgentRegistry()
    analyzer = IntentAnalyzer()
    context = ContextManager()
    orchestrator = Orchestrator(registry, context, analyzer)

    analysis = orchestrator.analyze_request("hello", "conv1")
    assert analysis.intent == "hello"
    agents = orchestrator.list_agents()
    assert isinstance(agents, list) and agents
    result = orchestrator.execute_plan(str(analysis.id))
    assert result["status"] == "completed"
