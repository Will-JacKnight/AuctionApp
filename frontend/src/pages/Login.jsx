import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
 
function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
 
  const handleLogin = (e) => {
    e.preventDefault();
    setLoading(true);
 
    // Mock login logic, you can replace it with actual API logic
    if (email === 'user@example.com' && password === 'password123') {
      navigate('/dashboard');
    } else {
      alert('Invalid credentials');
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
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
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