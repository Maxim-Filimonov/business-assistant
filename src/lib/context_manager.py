from __future__ import annotations

from typing import Dict
from src.models.context import Context


class ContextManager:
    """Simple in-memory context manager."""

    def __init__(self) -> None:
        self._conversations: Dict[str, Context] = {}

    def add_message(self, conversation_id: str, role: str, content: str) -> None:
        context = self._conversations.setdefault(conversation_id, Context(conversation_id))
        context.add_message(role, content)

    def get_context(self, conversation_id: str) -> Context:
        # Ensure that newly created conversations are stored so that
        # subsequent calls to ``get_context`` return the same instance and
        # retain any messages that may have been added directly to the
        # returned context.
        return self._conversations.setdefault(conversation_id, Context(conversation_id))
