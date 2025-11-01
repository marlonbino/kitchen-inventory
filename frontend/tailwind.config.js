/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // Enable class-based dark mode
  theme: {
    extend: {
      colors: {
        // High-contrast dark mode color tokens
        'dark-base': '#18181B', // Deep charcoal - base background
        'dark-card': '#262626', // Slightly lighter charcoal - cards/tables
        'dark-slate-base': '#1E293B', // Alternative deep charcoal
        'dark-slate-card': '#334155', // Alternative card background
        'text-primary': '#FFFFFF', // Pure white - primary text
        'text-secondary': '#D1D5DB', // Soft gray - secondary text
        'text-muted': '#9CA3AF', // Muted info text
        'accent-blue': '#3B82F6', // Electric blue - primary buttons
        'accent-blue-light': '#60A5FA', // Lighter electric blue
        'success-badge': '#34D399', // Vibrant green
        'warning-badge': '#FBBF24', // Neon orange/yellow
        'error-badge': '#F87171', // Neon/punchy red
        'error-badge-alt': '#EF4444', // Alternative error red
        'divider-blue': '#2563EB', // Soft blue for dividers
        'hover-row': '#404040', // Row hover state (neutral-700)
      },
      animation: {
        'slide-in': 'slideIn 0.3s ease-out',
        'slide-out': 'slideOut 0.3s ease-out',
      },
      keyframes: {
        slideIn: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(0)' },
        },
        slideOut: {
          '0%': { transform: 'translateX(0)' },
          '100%': { transform: 'translateX(-100%)' },
        },
      },
    },
  },
  plugins: [],
}

