import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './pages/Login';
import SignUp from './pages/SignUp';
import LandingPage from './pages/LandingPage';
import './styles/App.css';  // For styling
import Listing from './pages/Listing';
import Dashboard from './pages/Dashboard';
import Product from './pages/Product';
import ProtectedRoute from './components/ProtectedRoute';
 
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/" element={<LandingPage />} />
        <Route element={<ProtectedRoute />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/listing" element={<Listing />} />
        </Route>
        <Route path="/product/:id" element={<Product />} />
      </Routes>
    </Router>
  );
}
 
export default App;