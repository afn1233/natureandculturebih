import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      // Proxy all /api requests to the backend
      // This prevents CORS issues in development
      '/auth': {
        target: 'http://backend:8000',
        changeOrigin: true,
      },
      '/links': {
        target: 'http://backend:8000',
        changeOrigin: true,
      },
      '/chat': {
        target: 'http://backend:8000',
        changeOrigin: true,
      },
      '/webhook': {
        target: 'http://backend:8000',
        changeOrigin: true,
      },
      '/mcp': {
        target: 'http://backend:8000',
        changeOrigin: true,
      },
    }
  }
})