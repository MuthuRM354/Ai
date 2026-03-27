import logging
from functools import lru_cache

from fastapi import APIRouter, HTTPException

from src.application.use_cases.ask_chat import AskChatUseCase
from src.core.config import load_settings
from src.infrastructure.providers.anthropic_chat import AnthropicChatGateway
from src.presentation.api.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_chat_use_case() -> AskChatUseCase:
    settings = load_settings()
    gateway = AnthropicChatGateway(settings)
    return AskChatUseCase(gateway)


@router.get("/health")
def health():
    return {"status": "ok"}


@router.options("/chat")
def options_chat():
    return {"status": "ok"}


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        history = [m.model_dump() for m in req.history] if req.history else []
        answer = get_chat_use_case().execute(req.message, history)
        return ChatResponse(answer=answer)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    except RuntimeError as err:
        logger.exception("Chat service configuration error")
        raise HTTPException(
            status_code=500,
            detail="Chat service is not configured.",
        ) from err
    except Exception as err:
        logger.exception("Unexpected chat service error")
        raise HTTPException(status_code=500, detail="Internal server error") from err