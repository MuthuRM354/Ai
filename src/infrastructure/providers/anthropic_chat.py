from langchain_anthropic  import ChatAnthropic
from src.core.config import settings

class AnthropicChatGateway:
    def __init__(self, settings: settings):
        self.llm = ChatAnthropic(
            model=settings.anthropic_model,
            temperature=0,
            anthropic_api_key=settings.anthropic_api_key,
        )

    def ask(self, message: str) -> str:
        response = self.llm.invoke(message)
        return response.content