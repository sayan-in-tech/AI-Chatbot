import { useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import { useChatStore } from '../store/chatStore';

export function ChatWindow() {
  const messages = useChatStore((s) => s.messages);
  const isLoading = useChatStore((s) => s.isLoading);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    ref.current?.scrollTo({ top: ref.current.scrollHeight, behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div ref={ref} className="max-h-[65vh] overflow-y-auto pr-2">
      {messages.length === 0 && (
        <div className="text-white/60 text-sm">Start chatting with your selected persona.</div>
      )}
      <div className="space-y-3">
        {messages.map((m) => (
          <div key={m.id} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div
              className={`rounded-2xl px-4 py-2 max-w-[80%] border backdrop-blur-md ${
                m.role === 'user'
                  ? 'bg-white/15 border-white/20 shadow-[0_8px_32px_rgba(0,0,0,0.25)]'
                  : 'bg-white/10 border-white/15 shadow-[0_8px_32px_rgba(0,0,0,0.2)]'
              }`}
            >
              <div className="text-xs text-white/50 mb-1">
                {m.role === 'user' ? 'You' : 'Assistant'}
              </div>
              <div className="prose-invert markdown text-sm leading-relaxed">
                <ReactMarkdown>{m.content}</ReactMarkdown>
              </div>
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


