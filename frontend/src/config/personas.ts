import type { Persona } from '../types';

export const personas: readonly Persona[] = [
  {
    id: 'general',
    name: 'General',
    system:
      'You are a helpful assistant. Your task is to assist the user with their queries.',
  },
  {
    id: 'doctor',
    name: 'Doctor',
    system: 'You are a doctor. Your task is to assist the user with their queries.',
  },
  {
    id: 'programmer',
    name: 'Programmer',
    system:
      'You are a programmer. Your task is to assist the user with their queries.',
  },
];


