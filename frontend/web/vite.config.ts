import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Configuración básica para Vite + React + Tailwind
export default defineConfig({
  base: '/',
  plugins: [react()],
  build: {
    outDir: 'dist'
  },
  server: {
    port: 3000
  }
})

