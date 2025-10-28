import type { Config } from 'tailwindcss';

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        accent: {
          DEFAULT: '#f59e0b',
          500: '#f59e0b',
        },
        brandYellow: '#fbbf24',
        brandOrange: '#f59e0b',
        brandGray: '#9ca3af',
      },
      boxShadow: {
        glass: '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
      },
      backdropBlur: {
        xl: '20px',
      },
    },
  },
  plugins: [],
} satisfies Config;


