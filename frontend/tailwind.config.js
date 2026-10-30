/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: '#191A1A',
        surface: {
          DEFAULT: '#202222',
          hover: '#272A2A',
          active: '#2E3232',
          subtle: '#141515',
        },
        border: {
          DEFAULT: '#2D3131',
          light: '#3A3F3F',
          subtle: '#222525',
        },
        primary: {
          DEFAULT: '#20808D', // Perplexity teal
          hover: '#1B6E7A',
          light: '#289FA9',
          muted: 'rgba(32, 128, 141, 0.15)',
        },
        text: {
          primary: '#EBEBEB',
          secondary: '#A3A3A3',
          muted: '#6E7173',
        }
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
        display: ['Inter', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.25s ease-out forwards',
        'pulse-subtle': 'pulseSubtle 2s infinite ease-in-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(6px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        pulseSubtle: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.6' },
        }
      }
    },
  },
  plugins: [],
}

