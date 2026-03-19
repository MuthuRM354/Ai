from typing import Protocol

class ChatGateway(Protocol):
    def send_message(self, message: str) -> str:
        """Sends a message to the chat model and returns the response."""
        pass