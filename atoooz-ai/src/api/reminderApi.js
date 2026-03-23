const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

async function request(path, options = {}) {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  const data = res.status === 204 ? null : await res.json().catch(() => ({}));

  if (!res.ok) {
    throw new Error(data?.detail || "Request failed");
  }

  return data;
}

export function getRemindersApi() {
  return request("/reminders");
}

export function createReminderApi(payload) {
  return request("/reminders", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function updateReminderApi(id, payload) {
  return request(`/reminders/${id}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export function deleteReminderApi(id) {
  return request(`/reminders/${id}`, {
    method: "DELETE",
  });
}

export function extractReminderApi(message) {
  return request("/reminders/extract-and-create", {
    method: "POST",
    body: JSON.stringify({ message }),
  });
}