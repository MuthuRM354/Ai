# My AI Project

Local AI chat assistant with a FastAPI backend and a React + Vite frontend.

## Project structure
- `src/` - backend API, application logic, provider integrations
- `atoooz-ai/` - frontend chat UI
- `data/` - local reminder storage
- `tests/` - backend smoke/regression tests
- `main.py` - CLI entrypoint
- `src/api.py` - FastAPI entrypoint

## Features
- Multi-chat frontend UI
- AI chat endpoint backed by Anthropic via LangChain
- Local reminders with create, extract, toggle, delete
- Reminder-aware chat flow: reminder-like prompts are routed to reminder extraction before normal AI chat

## Backend
### Requirements
Create a `.env` file in the repo root with:

```env
ANTHROPIC_API_KEY=your_key_here
ANTHROPIC_MODEL=claude-3-haiku-20240307
FRONTEND_ORIGIN=http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174