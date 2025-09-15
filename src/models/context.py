from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Message:
    role: str
    content: str


@dataclass
class Context:
    conversation_id: str
    messages: List[Message] = field(default_factory=list)

    def add_message(self, role: str, content: str) -> None:
        self.messages.append(Message(role=role, content=content))
