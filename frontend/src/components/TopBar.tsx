import { PersonaSelect } from './PersonaSelect';
import { useChatStore } from '../store/chatStore';

export function TopBar() {
  const exportChatJSON = useChatStore((s) => s.exportChatJSON);
  const clearChat = useChatStore((s) => s.clearChat);

  return (
    <div className="glass rounded-2xl p-3 md:p-4 flex items-center justify-between card-glass">
      <div className="flex items-center gap-3">
        <div className="h-3 w-3 rounded-full bg-accent shadow-[0_0_18px_2px_rgba(245,158,11,0.7)]" />
        <span className="text-lg md:text-2xl font-semibold text-white/90">
          AI Chatbot
        </span>
      </div>
      <div className="flex items-center gap-2 md:gap-3">
        <div className="select-wrap">
          <div className="select-label">Persona</div>
          <div className="select-box">
            <PersonaSelect />
            <svg className="select-chevron" viewBox="0 0 24 24" fill="currentColor" aria-hidden>
              <path d="M7 10l5 5 5-5z" />
            </svg>
          </div>
        </div>
        <button
          onClick={exportChatJSON}
          className="px-3 py-2 rounded-xl btn-glass transition-colors text-sm"
        >
          Export JSON
        </button>
        <button
          onClick={clearChat}
          className="px-3 py-2 rounded-xl btn-glass transition-colors text-sm"
        >
          Clear Chat
        </button>
      </div>
    </div>
  );
}


