/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        forest: '#1e3a2f',
        moss: '#2d5a3d',
        amber: '#c8893a',
        cream: '#f5f0e8',
        stone: '#b8a898',
        warm: '#e8ddd0',
      },
      fontFamily: {
        display: ['Playfair Display', 'serif'],
        body: ['DM Sans', 'sans-serif'],
      },
    },
  },
  plugins: [],
}