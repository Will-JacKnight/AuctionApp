import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
 

const API_URL =
  import.meta.env.RUN_MODE === "docker"
    ? import.meta.env.API_GATEWAY_DOCKER_URL
    : import.meta.env.RUN_MODE === "heroku"
    ? import.meta.env.API_GATEWAY_HEROKU_URL
    : import.meta.env.API_GATEWAY_LOCAL_URL;

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
          setError(data.error || "Signup failed");
      }
  } catch (err) {
      console.log(err)
      setError("Network error. Please try again.");
  }
 
    setLoading(false);
  };
 
  return (
    <div className="auth-form">
      <h2>Login</h2>
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