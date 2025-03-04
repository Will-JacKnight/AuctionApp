import { createRoot } from 'react-dom/client'
import './styles/index.css'
import App from './App.jsx'
import { setApiUrl } from './config'

// Allow runtime injection of API URL
if (window.API_URL) {
  setApiUrl(window.API_URL);
}

createRoot(document.getElementById('root')).render(
    <App />
)
