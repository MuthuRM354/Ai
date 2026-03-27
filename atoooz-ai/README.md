# Atoooz AI Frontend

React + Vite frontend for the local AI chat assistant.

## What it does
- Chat UI with multiple local chat threads
- Reminder sidebar with create, toggle, delete
- Reminder-aware chat flow:
  - If a message looks like a reminder command, the frontend calls the reminder extraction endpoint first
  - On successful reminder extraction, it shows a confirmation message and skips the normal AI chat request
  - Otherwise it sends the chat request to the backend AI endpoint

## Key files
- `src/features/chat/ChatPage.jsx` - main page composition
- `src/store/slices/chatSlice.js` - chat state and async send flow
- `src/store/slices/reminderSlice.js` - reminder CRUD/extraction state
- `src/api/chatApi.js` - chat API wrapper
- `src/api/reminderApi.js` - reminder API wrapper
- `src/api/request.js` - shared request helper

## Commands
- `npm install`
- `npm run dev`
- `npm run lint`
- `npm run build`
- `npm run preview`

## Environment
Set `VITE_API_URL` if the backend is not running on the default:

- default backend URL: `http://127.0.0.1:8000`

Example `.env`:

```env
VITE_API_URL=http://127.0.0.1:8000