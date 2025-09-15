from src.services.intent_analyzer import IntentAnalyzer
from src.models.request import UserRequest


def test_intent_analyzer_returns_analysis():
    analyzer = IntentAnalyzer()
    req = UserRequest(text="schedule", conversation_id="c1")
    analysis = analyzer.analyze(req)
    assert analysis.intent == "schedule"
    assert analysis.request_id == req.id
