import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import "./../styles/authentication.css"
 

const API_URL = import.meta.env.VITE_API_RUN_MODE === "docker"
  ? import.meta.env.VITE_API_DOCKER_API_URL
  : import.meta.env.VITE_API_LOCAL_API_URL;

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
 
    try {
      const response = await fetch(`${API_URL}/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData)
      });

      const data = await response.json();
      if (response.ok) {
          console.log(data.access_token)
          alert("Login Successfull!");
          console.log(data.access_token)
          navigate("/"); // Redirect to login page
      } else {
          if(response.status == 401 || response.status == 404) {
              setError("Bad credentials. Please try again")
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
    <div className="auth-form form">
      <h2>Login</h2>
      {error && <p className="error-message">{error}</p>}
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Email"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={formData.password}
          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      <p>Don't have an account? <a href="/signup">Sign Up</a></p>
    </div>
  );
}
 
export default Login;