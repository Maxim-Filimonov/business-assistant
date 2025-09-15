from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Dict
import uuid


@dataclass
class UserRequest:
    """Represents a user request coming into the system."""

    text: str
    conversation_id: str
    user_id: Optional[str] = None
    metadata: Optional[Dict] = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self) -> None:
        if not self.text:
            raise ValueError("text cannot be empty")
