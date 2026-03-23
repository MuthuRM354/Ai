from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import load_settings
from src.presentation.api.routes.chat import router as chat_router
from src.presentation.api.routes.reminders import router as reminder_router


def create_app() -> FastAPI:
    settings = load_settings()

    app = FastAPI(title="AI Chat API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(chat_router)
    app.include_router(reminder_router)
    return app


app = create_app()