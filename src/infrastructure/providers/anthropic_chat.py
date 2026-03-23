from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from src.core.config import Settings


class AnthropicChatGateway:
    def __init__(self, settings: Settings):
        self.llm = ChatAnthropic(
            model=settings.anthropic_model,
            temperature=0,
            api_key=settings.anthropic_api_key,
        )

    def ask(self, message: str, history: list = None) -> str:
        messages = [
           SystemMessage(
    content=(
        "You are a helpful AI companion. "
        "This app can create reminders and tasks for the user. "
        "If the user asks to create a reminder, do not claim that reminders are impossible. "
        "If the app already handled the reminder, continue naturally."
    )
)
        ]

        for msg in (history or []):
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))

        messages.append(HumanMessage(content=message))

        response = self.llm.invoke(messages)
        return response.content