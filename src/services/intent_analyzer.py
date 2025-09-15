from __future__ import annotations

from typing import Optional, Dict
from src.models.request import UserRequest
from src.models.analysis import AnalysisResult


class IntentAnalyzer:
    """Simple placeholder intent analyzer."""

    def analyze(self, request: UserRequest, context: Optional[Dict] = None) -> AnalysisResult:
        intent = request.text.strip()
        return AnalysisResult(
            request_id=request.id,
            intent=intent,
            confidence=0.5,
            required_agents=[],
            requires_clarification=False,
            clarification_options=[],
            context_used=context or {},
            execution_plan="",
        )
