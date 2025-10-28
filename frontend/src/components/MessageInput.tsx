import { useState } from 'react';
import { useChatStore } from '../store/chatStore';

export function MessageInput() {
  const [text, setText] = useState('');
  const sendMessage = useChatStore((s) => s.sendMessage);
  const isLoading = useChatStore((s) => s.isLoading);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const toSend = text;
    setText('');
    await sendMessage(toSend);
  };

  return (
    <form onSubmit={onSubmit} className="glass rounded-2xl p-2 flex items-center gap-2">
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type your message..."
        className="flex-1 bg-transparent outline-none px-3 py-2 text-sm"
      />
      <button
        disabled={isLoading || !text.trim()}
        className="px-4 py-2 rounded-xl btn-glass disabled:opacity-50 disabled:cursor-not-allowed text-black text-sm font-medium"
      >
        Send
      </button>
    </form>
  );
}


