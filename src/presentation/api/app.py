from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import load_settings
from src.presentation.api.routes.chat import router as chat_router
from src.presentation.api.routes.reminders import router as reminder_router


def _normalize_origins(raw: str) -> list[str]:
    origins = []
    for o in (raw or "").split(","):
        o = o.strip().rstrip("/")
        if o:
            origins.append(o)
    return origins


def create_app() -> FastAPI:
    settings = load_settings()
    app = FastAPI(title="AI Chat API")

    allowed_origins = _normalize_origins(settings.frontend_origin)
    if not allowed_origins:
        allowed_origins = [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:5174",
            "http://127.0.0.1:5174",
        ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    app.include_router(chat_router)
    app.include_router(reminder_router)
    return app


app = create_app()