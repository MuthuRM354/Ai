from typing import Any, Protocol

class ChatGateway(Protocol):
   def ask(self, message: str, history: list[dict[str, Any]] | None = None) -> str:
        """Sends a message (with optional history) and returns the response."""
        pass