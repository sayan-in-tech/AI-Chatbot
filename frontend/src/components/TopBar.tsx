import { PersonaSelect } from './PersonaSelect';
import { useChatStore } from '../store/chatStore';

export function TopBar() {
  const exportChatJSON = useChatStore((s) => s.exportChatJSON);
  const clearChat = useChatStore((s) => s.clearChat);

  return (
    <div className="glass rounded-2xl p-3 md:p-4 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="h-3 w-3 rounded-full bg-accent shadow-[0_0_20px_2px_rgba(34,211,238,0.8)]" />
        <span className="text-sm md:text-base font-medium text-white/90">
          AI Chatbot
        </span>
      </div>
      <div className="flex items-center gap-2 md:gap-3">
        <PersonaSelect />
        <button
          onClick={exportChatJSON}
          className="px-3 py-2 rounded-xl bg-white/10 border border-white/15 hover:bg-white/15 transition-colors text-sm"
        >
          Export JSON
        </button>
        <button
          onClick={clearChat}
          className="px-3 py-2 rounded-xl bg-white/10 border border-white/15 hover:bg-white/15 transition-colors text-sm"
        >
          Clear Chat
        </button>
      </div>
    </div>
  );
}


