from src.lib.context_manager import ContextManager


def test_context_manager_stores_messages():
    cm = ContextManager()
    cm.add_message("conv", "user", "hi")
    context = cm.get_context("conv")
    assert context.messages[0].content == "hi"
