from src.domain.gateways.chat_gateway import ChatGateway

class AskChatUseCase:
    def __init__(self, chat_gateway: ChatGateway):
        self.chat_gateway = chat_gateway

    def execute(self, message: str) -> str:
        if not message or not message.strip():
            raise ValueError("Message cannot be empty.")
        return self.chat_gateway.ask(message.strip())