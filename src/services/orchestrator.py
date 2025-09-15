from __future__ import annotations

from typing import Optional, Dict, List

from src.services.intent_analyzer import IntentAnalyzer
from src.services.agent_registry import AgentRegistry
from src.lib.context_manager import ContextManager
from src.models.analysis import AnalysisResult
from src.models.request import UserRequest


class Orchestrator:
    """Coordinates intent analysis and agent execution."""

    def __init__(self, agent_registry: AgentRegistry, context_manager: ContextManager, intent_analyzer: IntentAnalyzer) -> None:
        self.agent_registry = agent_registry
        self.context_manager = context_manager
        self.intent_analyzer = intent_analyzer
        self._analyses: Dict[str, AnalysisResult] = {}

    def analyze_request(self, text: str, conversation_id: str, user_id: Optional[str] = None, metadata: Optional[Dict] = None) -> AnalysisResult:
        if not text:
            raise ValueError("text cannot be empty")
        request = UserRequest(text=text, conversation_id=conversation_id, user_id=user_id, metadata=metadata)
        context = self.context_manager.get_context(conversation_id)
        analysis = self.intent_analyzer.analyze(request, context_used_to_dict(context))
        self._analyses[str(analysis.id)] = analysis
        return analysis

    def execute_plan(self, analysis_id: str, async_mode: bool = False) -> Dict:
        if analysis_id not in self._analyses:
            raise KeyError("analysis_id not found")
        return {
            "id": analysis_id,
            "status": "completed",
            "result": {},
            "errors": [],
            "execution_time": 0.0,
        }

    def clarify_request(self, analysis_id: str, selected_option: str, additional_context: Optional[str] = None) -> AnalysisResult:
        raise NotImplementedError

    def list_agents(self) -> List:
        return self.agent_registry.list_agents()

    def get_execution_status(self, execution_id: str) -> Dict:
        raise NotImplementedError


def context_used_to_dict(context) -> Dict:
    """Helper to convert Context to dict for analysis"""
    return {"messages": [ {"role": m.role, "content": m.content} for m in context.messages ]}
