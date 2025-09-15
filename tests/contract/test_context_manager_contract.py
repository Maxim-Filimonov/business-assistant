from src.lib.context_manager import ContextManager


def test_context_manager_stores_messages():
    cm = ContextManager()
    cm.add_message("conv", "user", "hi")
    context = cm.get_context("conv")
    assert context.messages[0].content == "hi"


def test_get_context_persists_new_conversations():
    cm = ContextManager()
    # Retrieve a context that doesn't yet exist
    context = cm.get_context("new_conv")
    # Mutate the context directly
    context.add_message("user", "hello")
    # Subsequent retrieval should return the same context with the message
    persisted = cm.get_context("new_conv")
    assert persisted.messages[0].content == "hello"
