import { useEffect, useMemo, useState } from 'react';
import { checkBackendConnectivity, type Connectivity } from '../services/api';

export function HealthIndicator() {
  const [conn, setConn] = useState<Connectivity>('offline');
  const [latencyMs, setLatencyMs] = useState<number | null>(null);
  const [lastChecked, setLastChecked] = useState<number | null>(null);

  const color = useMemo(() => {
    return conn === 'online'
      ? 'bg-green-500 shadow-[0_0_12px_2px_rgba(34,197,94,0.7)]'
      : 'bg-red-500 shadow-[0_0_12px_2px_rgba(239,68,68,0.7)]';
  }, [conn]);

  async function runCheck() {
    const t0 = performance.now();
    const s = await checkBackendConnectivity();
    const t1 = performance.now();
    setConn(s);
    setLatencyMs(Math.round(t1 - t0));
    setLastChecked(Date.now());
  }

  useEffect(() => {
    runCheck();
    const id = setInterval(runCheck, 5000);
    return () => clearInterval(id);
  }, []);

  const label = useMemo(() => (conn === 'online' ? 'Backend: Connected' : 'Backend: Disconnected'), [conn]);

  return (
    <button
      onClick={runCheck}
      title={`${label}${latencyMs != null ? ` • ${latencyMs}ms` : ''}${lastChecked ? ` • ${new Date(lastChecked).toLocaleTimeString()}` : ''}`}
      className="fixed top-2 left-2 z-50 select-none"
      aria-label={label}
    >
      <div className="glass rounded-xl px-2.5 py-1.5 flex items-center gap-2 border border-white/10">
        <span className={`inline-block h-2.5 w-2.5 rounded-full ${color}`} />
        <span className="text-xs text-white/90">{label}</span>
        {latencyMs != null && (
          <span className="text-[10px] text-white/60">{latencyMs}ms</span>
        )}
      </div>
    </button>
  );
}


