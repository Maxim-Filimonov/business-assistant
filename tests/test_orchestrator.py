import importlib
import sys
import types

import pytest


@pytest.fixture(autouse=True)
def stub_crewai(monkeypatch):
    fake_crewai = types.ModuleType("crewai")

    class FakeProcess:
        sequential = "sequential"
        hierarchical = "hierarchical"

    class FakeTask:
        def __init__(self, description, agent=None, expected_output=None):
            self.description = description
            self.agent = agent
            self.expected_output = expected_output

    class FakeAgent:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

    class RecordingCrew:
        instances = []
        kickoff_behavior = None

        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs
            RecordingCrew.instances.append(self)

        def kickoff(self):
            if RecordingCrew.kickoff_behavior is not None:
                return RecordingCrew.kickoff_behavior(self)
            return {"final_output": "planned"}

    fake_crewai.Process = FakeProcess
    fake_crewai.Task = FakeTask
    fake_crewai.Agent = FakeAgent
    fake_crewai.Crew = RecordingCrew

    fake_tools = types.ModuleType("crewai.tools")

    class BaseTool:
        def __init__(self, *args, **kwargs):
            pass

        def __call__(self, *args, **kwargs):  # pragma: no cover - safety shim
            return self._run(*args, **kwargs)

    fake_tools.BaseTool = BaseTool

    monkeypatch.setitem(sys.modules, "crewai", fake_crewai)
    monkeypatch.setitem(sys.modules, "crewai.tools", fake_tools)

    fake_pypdf2 = types.ModuleType("PyPDF2")

    class DummyPdfReader:
        def __init__(self, *args, **kwargs):
            self.pages = []

    fake_pypdf2.PdfReader = DummyPdfReader
    monkeypatch.setitem(sys.modules, "PyPDF2", fake_pypdf2)

    class DummyPdfContext:
        def __init__(self):
            self.pages = []

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            return False

    fake_pdfplumber = types.ModuleType("pdfplumber")
    fake_pdfplumber.open = lambda *args, **kwargs: DummyPdfContext()
    monkeypatch.setitem(sys.modules, "pdfplumber", fake_pdfplumber)

    yield RecordingCrew

    RecordingCrew.instances.clear()
    RecordingCrew.kickoff_behavior = None


@pytest.fixture
def chat_system(monkeypatch, stub_crewai):
    monkeypatch.setattr("config.get_llm", lambda provider=None: "llm")

    import agents.crm_agent as crm_agent_module
    import agents.scheduler_agent as scheduler_agent_module
    import agents.invoice_agent as invoice_agent_module
    import agents.dispatcher_agent as dispatcher_agent_module
    import orchestrator as orchestrator_module
    import main as main_module

    for module in [
        crm_agent_module,
        scheduler_agent_module,
        invoice_agent_module,
        dispatcher_agent_module,
        orchestrator_module,
        main_module,
    ]:
        importlib.reload(module)

    return main_module.FlexibleBusinessChat(), main_module, stub_crewai


def test_orchestrator_uses_planning(chat_system):
    chat, main_module, crew_cls = chat_system
    crew_cls.instances.clear()

    def orchestrated_response(_instance):
        return {"final_output": "orchestrated result"}

    crew_cls.kickoff_behavior = orchestrated_response

    result = chat.process_request("Prepare a schedule and invoice overview")

    assert result == "orchestrated result"
    assert crew_cls.instances, "No crew was created for orchestrator processing"

    orchestrator_instance = crew_cls.instances[0]
    assert orchestrator_instance.kwargs["process"] == main_module.Process.hierarchical
    assert orchestrator_instance.kwargs["planning"] is True
    task = orchestrator_instance.kwargs["tasks"][0]
    assert "Prepare a schedule and invoice overview" in task.description


def test_orchestrator_falls_back_on_failure(chat_system):
    chat, main_module, crew_cls = chat_system
    crew_cls.instances.clear()

    def behavior(instance):
        if instance.kwargs["process"] == main_module.Process.hierarchical:
            raise RuntimeError("boom")
        return "scheduler success"

    crew_cls.kickoff_behavior = behavior

    result = chat.process_request("Need schedule updates")

    assert result == "Schedule Analysis: scheduler success"
    assert len(crew_cls.instances) >= 2
    assert any(
        inst.kwargs["process"] == main_module.Process.sequential
        for inst in crew_cls.instances[1:]
    )
