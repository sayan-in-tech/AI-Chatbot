export type Role = 'user' | 'assistant' | 'system';

export interface Message {
  id: string;
  role: Role;
  content: string;
  createdAt: number;
}

export interface Persona {
  id: 'general' | 'doctor' | 'programmer';
  name: string;
  system: string;
}


