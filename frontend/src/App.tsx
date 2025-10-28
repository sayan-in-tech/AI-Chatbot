import { TopBar } from './components/TopBar';
import { ChatWindow } from './components/ChatWindow';
import { MessageInput } from './components/MessageInput';
import { FluidCursor } from './components/FluidCursor';
import { HealthIndicator } from './components/HealthIndicator';

export function App() {
  return (
    <div className="relative min-h-dvh text-white">
      <HealthIndicator />
      <FluidCursor />
      <div className="mx-auto max-w-5xl px-4 py-6">
        <TopBar />
        <div className="mt-6 glass rounded-2xl p-4 md:p-6">
          <ChatWindow />
        </div>
        <div className="sticky bottom-4 mt-4">
          <MessageInput />
        </div>
      </div>
    </div>
  );
}


