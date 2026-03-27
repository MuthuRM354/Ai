from fastapi.testclient import TestClient

from src.presentation.api.app import app
from src.presentation.api.routes import reminders as reminder_routes
from src.presentation.api.routes import chat as chat_routes


class FakeUseCase:
    def execute(self, message: str, history: list | None = None) -> str:
        return f"Echo: {message}"


client = TestClient(app)


def setup_function():
    reminder_routes._store.clear()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_success(monkeypatch):
    monkeypatch.setattr(chat_routes, "get_chat_use_case", lambda: FakeUseCase())

    response = client.post(
        "/chat",
        json={
            "message": "hello",
            "history": [{"role": "user", "content": "hi"}],
        },
    )

    assert response.status_code == 200
    assert response.json() == {"answer": "Echo: hello"}


def test_chat_rejects_invalid_role():
    response = client.post(
        "/chat",
        json={
            "message": "hello",
            "history": [{"role": "system", "content": "bad"}],
        },
    )

    assert response.status_code == 422


def test_create_toggle_delete_reminder():
    create_response = client.post(
        "/reminders",
        json={"title": "Buy milk", "due_at": None},
    )
    assert create_response.status_code == 200
    reminder = create_response.json()
    reminder_id = reminder["id"]
    assert reminder["title"] == "Buy milk"
    assert reminder["completed"] is False

    list_response = client.get("/reminders")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    update_response = client.patch(
        f"/reminders/{reminder_id}",
        json={"completed": True},
    )
    assert update_response.status_code == 200
    assert update_response.json()["completed"] is True

    delete_response = client.delete(f"/reminders/{reminder_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"status": "deleted"}


def test_extract_and_create_reminder():
    response = client.post(
        "/reminders/extract-and-create",
        json={"message": "remind me tomorrow at 9am to call mom"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["matched"] is True
    assert payload["reminder"]["title"] == "call mom"