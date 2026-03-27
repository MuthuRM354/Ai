import { apiRequest } from "./request";

export async function sendChatMessage(message, history = []) {
  const data = await apiRequest("/chat", {
    method: "POST",
    body: JSON.stringify({ message, history }),
  });

  return data.answer;
}