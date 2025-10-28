import { useEffect, useRef } from 'react';
import { useChatStore } from '../store/chatStore';

export function ChatWindow() {
  const messages = useChatStore((s) => s.messages);
  const isLoading = useChatStore((s) => s.isLoading);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    ref.current?.scrollTo({ top: ref.current.scrollHeight, behavior: 'smooth' });
  }, [messages.length, isLoading]);

  return (
    <div ref={ref} className="max-h-[65vh] overflow-y-auto pr-2">
      {messages.length === 0 && (
        <div className="text-white/60 text-sm">Start chatting with your selected persona.</div>
      )}
      <div className="space-y-3">
        {messages.map((m) => (
          <div key={m.id} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div
              className={`rounded-2xl px-4 py-2 max-w-[80%] border ${
                m.role === 'user'
                  ? 'bg-white/15 border-white/20'
                  : 'bg-white/8 border-white/15'
              }`}
            >
              <div className="text-xs text-white/50 mb-1">
                {m.role === 'user' ? 'You' : 'Assistant'}
              </div>
              <div className="whitespace-pre-wrap text-sm leading-relaxed">{m.content}</div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="text-white/60 text-sm">Assistant is typing…</div>
        )}
      </div>
    </div>
  );
}


