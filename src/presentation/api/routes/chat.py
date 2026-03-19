from fastapi import APIRouter, HTTPException
from src.application.use_cases.ask_chat import AskChatUseCase
from src.core.config import load_settings
from src.infrastructure.providers.anthropic_chat import AnthropicChatGateway
from src.presentation.api.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()

settings = load_settings()
gateway = AnthropicChatGateway(settings)
use_case = AskChatUseCase(gateway)


@router.get("/health")
def health():
    return {"status": "ok"}


@router.options("/chat")
def options_chat():
    return {"status": "ok"}


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        answer = use_case.execute(req.message)
        return ChatResponse(answer=answer)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))