const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export async function sendChatMessage(message) {
 
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'},
      body: JSON.stringify({ message }),
    });

    const data = await response.json();
    if (!response.ok) 
      throw new Error(data.detail || 'Failed to send message');
      return data.answer;
}
