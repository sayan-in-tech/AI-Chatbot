interface ChatPayloadMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

interface ChatRequestPayload {
  system: string;
  messages: ChatPayloadMessage[];
}

export async function chatRequest(payload: ChatRequestPayload): Promise<string> {
  const base = import.meta.env.VITE_API_BASE_URL ?? '';
  const res = await fetch(`${base}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    throw new Error(`Chat request failed: ${res.status}`);
  }
  const data = await res.json();
  return data.reply as string;
}


