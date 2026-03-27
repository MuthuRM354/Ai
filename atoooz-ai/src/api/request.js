const DEFAULT_API_URL = "http://127.0.0.1:8000";
const API_URL = (import.meta.env.VITE_API_URL || DEFAULT_API_URL).replace(/\/$/, "");
const REQUEST_TIMEOUT_MS = 15000;

async function parseJsonSafely(response) {
  if (response.status === 204) return null;

  const text = await response.text();
  if (!text) return {};

  try {
    return JSON.parse(text);
  } catch {
    return {};
  }
}

export async function apiRequest(path, options = {}) {
  const controller = new AbortController();
  let timedOut = false;

  const timeoutId = setTimeout(() => {
    timedOut = true;
    controller.abort();
  }, REQUEST_TIMEOUT_MS);

  try {
    const response = await fetch(`${API_URL}${path}`, {
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
      ...options,
      signal: options.signal ?? controller.signal,
    });

    const data = await parseJsonSafely(response);

    if (!response.ok) {
      throw new Error(data?.detail || `Request failed with status ${response.status}`);
    }

    return data;
  } catch (error) {
    if (error.name === "AbortError") {
      throw new Error(
        timedOut ? "Request timed out. Please try again." : "Request was cancelled."
      );
    }

    throw error;
  } finally {
    clearTimeout(timeoutId);
  }
}