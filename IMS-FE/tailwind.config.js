/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'media', // theo system
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      container: { center: true, padding: '1rem' }
    },
  },
  plugins: [],
}
