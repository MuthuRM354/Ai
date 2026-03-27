import json
import logging
import re
from datetime import UTC, datetime, timedelta
from itertools import count
from pathlib import Path
from threading import Lock
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.presentation.api.schemas.reminder import (
    ReminderCreate,
    ReminderOut,
    ReminderUpdate,
)

router = APIRouter(prefix="/reminders", tags=["reminders"])
logger = logging.getLogger(__name__)

_lock = Lock()
_DATA_FILE = Path(__file__).resolve().parents[4] / "data" / "reminders.json"


def _load_store() -> list[ReminderOut]:
    if not _DATA_FILE.exists():
        return []

    try:
        raw = json.loads(_DATA_FILE.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            logger.warning("Reminder store is not a list. Resetting in-memory store.")
            return []
        return [ReminderOut.model_validate(item) for item in raw]
    except Exception:
        logger.exception("Failed to load reminder store from disk")
        return []


def _save_store(items: list[ReminderOut]) -> None:
    _DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    payload = [item.model_dump(mode="json") for item in items]
    _DATA_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")


_store: list[ReminderOut] = _load_store()
_next_id = max((item.id for item in _store), default=0) + 1
_id_gen = count(_next_id)


class ReminderExtractRequest(BaseModel):
    message: str


class ReminderExtractResponse(BaseModel):
    matched: bool
    reminder: Optional[ReminderOut] = None
    extracted_title: Optional[str] = None
    extracted_due_at: Optional[datetime] = None


def _parse_time_portion(text: str) -> tuple[Optional[int], Optional[int]]:
    text = text.lower().strip()

    match = re.search(r"\b(?:at\s*)?(\d{1,2})(?::(\d{2}))?\s*(am|pm)\b", text)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2) or 0)
        meridiem = match.group(3)

        if meridiem == "pm" and hour != 12:
            hour += 12
        if meridiem == "am" and hour == 12:
            hour = 0
        return hour, minute

    match_24 = re.search(r"\b(?:at\s*)?(\d{1,2}):(\d{2})\b", text)
    if match_24:
        return int(match_24.group(1)), int(match_24.group(2))

    return None, None


def _extract_reminder_details(message: str) -> tuple[bool, Optional[str], Optional[datetime]]:
    text = message.strip()
    lower = text.lower()

    if "remind me" not in lower:
        return False, None, None

    now = datetime.now()
    due_at = None

    hour, minute = _parse_time_portion(lower)

    base_date = None
    if "tomorrow" in lower:
        base_date = (now + timedelta(days=1)).date()
    elif "today" in lower:
        base_date = now.date()

    if base_date and hour is not None:
        due_at = datetime.combine(base_date, datetime.min.time()).replace(
            hour=hour,
            minute=minute or 0,
            second=0,
            microsecond=0,
        )
    elif base_date:
        due_at = datetime.combine(base_date, datetime.min.time()).replace(
            hour=9,
            minute=0,
            second=0,
            microsecond=0,
        )

    title = text

    patterns = [
        r"remind me\s+(?:today|tomorrow)?\s*(?:at\s*)?\d{0,2}(?::\d{2})?\s*(?:am|pm)?\s*to\s+(.+)",
        r"remind me\s+to\s+(.+)",
        r"remind me\s+(?:today|tomorrow)\s+(.+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, lower, re.IGNORECASE)
        if match:
            extracted = match.group(1).strip(" .")
            if extracted:
                title = extracted
                break

    title = re.sub(r"\s+", " ", title).strip()

    if not title:
        return False, None, None

    return True, title, due_at


@router.get("", response_model=list[ReminderOut])
def list_reminders():
    return sorted(_store, key=lambda r: (r.completed, r.due_at or datetime.max, r.created_at))


@router.post("", response_model=ReminderOut)
def create_reminder(payload: ReminderCreate):
    title = payload.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Reminder title cannot be empty")

    with _lock:
        item = ReminderOut(
            id=next(_id_gen),
            title=title,
            completed=False,
            due_at=payload.due_at,
            created_at=datetime.now(UTC),
        )
        _store.append(item)
        _save_store(_store)
        return item


@router.post("/extract-and-create", response_model=ReminderExtractResponse)
def extract_and_create_reminder(payload: ReminderExtractRequest):
    matched, title, due_at = _extract_reminder_details(payload.message)

    if not matched or not title:
        return ReminderExtractResponse(matched=False)

    with _lock:
        item = ReminderOut(
            id=next(_id_gen),
            title=title,
            completed=False,
            due_at=due_at,
            created_at=datetime.now(UTC),
        )
        _store.append(item)
        _save_store(_store)

    return ReminderExtractResponse(
        matched=True,
        reminder=item,
        extracted_title=title,
        extracted_due_at=due_at,
    )


@router.patch("/{reminder_id}", response_model=ReminderOut)
def update_reminder(reminder_id: int, payload: ReminderUpdate):
    with _lock:
        for idx, item in enumerate(_store):
            if item.id == reminder_id:
                updated = item.model_copy(update={"completed": payload.completed})
                _store[idx] = updated
                _save_store(_store)
                return updated
    raise HTTPException(status_code=404, detail="Reminder not found")


@router.delete("/{reminder_id}")
def delete_reminder(reminder_id: int):
    with _lock:
        for idx, item in enumerate(_store):
            if item.id == reminder_id:
                _store.pop(idx)
                _save_store(_store)
                return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Reminder not found")