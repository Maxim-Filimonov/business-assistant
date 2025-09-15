from src.lib.base_agent import BaseAgent


class DummyAgent(BaseAgent):
    def get_capabilities(self):
        return ["test"]

    def can_handle(self, intent, context):
        return {"can_handle": True, "confidence": 1.0, "reason": "always"}

    def execute_task(self, task_description, input_data, context):
        return {"success": True, "result": {}, "error": None}


def test_agent_interface_methods():
    agent = DummyAgent("id1", "dummy", "desc")
    assert agent.get_capabilities() == ["test"]
    result = agent.can_handle("anything", {})
    assert result["can_handle"] is True
    assert agent.execute_task("do", {}, {})["success"] is True
    assert agent.get_dependencies() == []
    status = agent.get_status()
    assert status["status"] == "available"
