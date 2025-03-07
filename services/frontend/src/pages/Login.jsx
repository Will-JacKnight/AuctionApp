import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import "./../styles/authentication.css"
import NavBar from '../components/NavBar';
// import { getApiUrl } from '../config';

const API_URL =
  import.meta.env.VITE_RUN_MODE === "docker"
    // When running in Docker, we access the frontend via localhost from the browser (external access)
    ? import.meta.env.VITE_API_GATEWAY_LOCAL_URL
    : import.meta.env.VITE_RUN_MODE === "heroku"
    ? import.meta.env.VITE_API_GATEWAY_HEROKU_URL
    : import.meta.env.VITE_API_GATEWAY_LOCAL_URL;

function Login() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const [error, setError] = useState();
 
  const handleLogin = async(e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
 
    try {
      const response = await fetch(`${API_URL}/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData)
      });

      const data = await response.json();
      if (response.ok) {
          sessionStorage.setItem("token", data.access_token)
          const lastVisited = sessionStorage.getItem("lastVisited") || "/dashboard"
          sessionStorage.removeItem("lastVisited")
          navigate(lastVisited)
      } else {
          if(response.status === 401 || response.status === 404) {
              setError("Invalid email or password. Please try again.")
          }
          else {
            setError(data.error || "Login failed");
          }
      }
    } catch (err) {
      console.log(err)
      setError("Network error. Please try again.");
    }
 
    setLoading(false);
  };
 
  return (
    <div className="min-h-screen bg-gray-50">
      <NavBar />
      <div className="auth-form">
        <h2>Welcome Back</h2>
        <p className="text-center text-gray-600 mb-6">Please sign in to your account</p>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleLogin}>
          <div className="form-group">
            <input
              type="email"
              placeholder="Email address"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              required
              autoComplete="email"
            />
          </div>
          
          <div className="form-group">
            <input
              type="password"
              placeholder="Password"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              required
              autoComplete="current-password"
            />
          </div>
          
          <button type="submit" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
        
        <p className="mt-6 text-center">
          Don't have an account?{' '}
          <Link to="/signup" className="text-blue-600 hover:text-blue-800">
            Create one now
          </Link>
        </p>
      </div>
    </div>
  );
}
 
export default Login;