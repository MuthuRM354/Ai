import os
from dotenv import load_dotenv
from dataclasses import dataclass


@dataclass
class Settings:
    anthropic_api_key: str
    anthropic_model: str
    frontend_origin: str


def load_settings() -> Settings:
    load_dotenv()

    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    if not anthropic_api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not found in .env")

    return Settings(
        anthropic_api_key=anthropic_api_key,
        anthropic_model=os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307"),
        frontend_origin=os.getenv("FRONTEND_ORIGIN", "http://localhost:5174"),
    )