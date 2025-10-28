import { create } from 'zustand';
import type { Message, Persona } from '../types';
import { personas } from '../config/personas';
import { chatRequest, chatRequestStream } from '../services/api';

interface ChatState {
  messages: Message[];
  persona: Persona;
  isLoading: boolean;
  sendMessage: (text: string) => Promise<void>;
  setPersona: (id: Persona['id']) => void;
  clearChat: () => void;
  exportChatJSON: () => void;
}

function createMessage(role: Message['role'], content: string): Message {
  return {
    id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    role,
    content,
    createdAt: Date.now(),
  };
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  persona: personas[0],
  isLoading: false,
  setPersona: (id) => {
    const next = personas.find((p) => p.id === id) ?? personas[0];
    set({ persona: next });
  },
  clearChat: () => set({ messages: [] }),
  exportChatJSON: () => {
    const { persona, messages } = get();
    const payload = {
      personaId: persona.id,
      system: persona.system,
      messages,
      exportedAt: new Date().toISOString(),
    };
    const blob = new Blob([JSON.stringify(payload, null, 2)], {
      type: 'application/json',
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    const date = new Date().toISOString().slice(0, 10).replace(/-/g, '');
    a.href = url;
    a.download = `chat-${date}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  },
  sendMessage: async (text: string) => {
    if (!text.trim()) return;
    const userMessage = createMessage('user', text.trim());
    set((s) => ({ messages: [...s.messages, userMessage], isLoading: true }));

    try {
      const { persona } = get();
      const sessionId = getOrCreateSessionId();
      // prepare an empty assistant message and stream into it
      const assistantId = `${Date.now()}-assistant-${Math.random()
        .toString(36)
        .slice(2, 8)}`;
      set((s) => ({
        messages: [
          ...s.messages,
          { id: assistantId, role: 'assistant', content: '', createdAt: Date.now() },
        ],
      }));

      await chatRequestStream(
        { message: text.trim(), session_id: sessionId, role: persona.id },
        (chunk) => {
          set((s) => ({
            messages: s.messages.map((m) =>
              m.id === assistantId ? { ...m, content: m.content + chunk } : m
            ),
          }));
        }
      );
    } finally {
      set({ isLoading: false });
    }
  },
}));

function getOrCreateSessionId(): string {
  const key = 'chat.session_id';
  let id = localStorage.getItem(key);
  if (!id) {
    id = `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
    localStorage.setItem(key, id);
  }
  return id;
}


