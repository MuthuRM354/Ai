import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic


def get_llm():
    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not found in .env")

    model_name = os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307")

    return ChatAnthropic(
        model=model_name,
        temperature=0,
        api_key=api_key,
    )