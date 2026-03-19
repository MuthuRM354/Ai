from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import load_settings
from src.presentation.api.routes.chat import router as chat_router


def create_app() -> FastAPI:
    settings = load_settings()

    app = FastAPI(title="AI Chat API")
    
    # Add CORS middleware BEFORE routes
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins during development
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(chat_router)
    return app


app = create_app()