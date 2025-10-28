export interface ChatRequestPayload {
  message: string;
  session_id: string;
  role: string; // 'general' | 'doctor' | 'programmer'
}

export async function chatRequest(payload: ChatRequestPayload): Promise<string> {
  const base = import.meta.env.VITE_API_BASE_URL ?? '';
  const res = await fetch(`${base}/api/v1/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    throw new Error(`Chat request failed: ${res.status}`);
  }
  const data = await res.json();
  return (data.response as string) ?? '';
}

// Streaming helper
export async function chatRequestStream(
  payload: ChatRequestPayload,
  onChunk: (text: string) => void
): Promise<void> {
  const base = import.meta.env.VITE_API_BASE_URL ?? '';
  const res = await fetch(`${base}/api/v1/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'text/event-stream, text/plain, application/octet-stream',
    },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`Chat request failed: ${res.status}`);

  // If server sent JSON, fall back to non-stream
  const contentType = res.headers.get('content-type') || '';
  if (contentType.includes('application/json')) {
    const data = await res.json();
    const full = String(data?.response || '');
    if (full) {
      // Simulate streaming so the UI proves the path works
      const parts = full.split(/(\s+)/); // keep spaces
      for (const part of parts) {
        onChunk(part);
        // small delay to visualize
        // eslint-disable-next-line no-await-in-loop
        await new Promise((r) => setTimeout(r, 15));
      }
    }
    return;
  }

  const reader = res.body?.getReader();
  if (!reader) return;
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    // Try to parse SSE lines; keep incomplete line in buffer
    let lastNewline = buffer.lastIndexOf('\n');
    if (lastNewline === -1) continue;
    const chunk = buffer.slice(0, lastNewline);
    buffer = buffer.slice(lastNewline + 1);

    const lines = chunk.split(/\r?\n/);
    let emitted = false;
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed) continue;
      if (trimmed.startsWith('data:')) {
        const data = trimmed.slice(5).trim();
        if (data && data !== '[DONE]') {
          // console.debug('[stream:data]', data);
          onChunk(data);
          emitted = true;
        }
      } else {
        // Fallback: treat as raw text
        // console.debug('[stream:raw]', trimmed);
        onChunk(trimmed);
        emitted = true;
      }
    }
  }

  // Flush any remaining buffer as plain text
  if (buffer.trim()) {
    // console.debug('[stream:flush]', buffer.trim());
    onChunk(buffer.trim());
  }
}


