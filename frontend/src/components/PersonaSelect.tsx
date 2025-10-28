import { personas } from '../config/personas';
import { useChatStore } from '../store/chatStore';

export function PersonaSelect() {
  const current = useChatStore((s) => s.persona);
  const setPersona = useChatStore((s) => s.setPersona);

  return (
    <select
      aria-label="Persona"
      value={current.id}
      onChange={(e) => setPersona(e.target.value as any)}
      className="select-glass text-sm"
    >
      {personas.map((p) => (
        <option key={p.id} value={p.id}>
          {p.name}
        </option>
      ))}
    </select>
  );
}


