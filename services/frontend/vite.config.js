import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
 
// https://vite.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      '@': '/src', // Alias to the src/ folder
    },
  },
  plugins: [react()],
  server: {
    port: process.env.PORT || 5173, // Use Heroku's dynamic $PORT or default to 5173 for local development
    host: '0.0.0.0', // Ensure Vite listens on all network interfaces
    allowedHosts: [
      "bidding-app-sse-6fcb4edfed53.herokuapp.com" // Allow your Heroku domain
    ],
  },
<<<<<<< HEAD
});
 
=======
});
>>>>>>> 0ca238e (feat/merge version1)
