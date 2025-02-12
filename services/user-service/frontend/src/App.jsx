import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './pages /Login';
import SignUp from './pages /SignUp';
import './App.css';  // For styling

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<div>Welcome to the Home Page</div>} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />
      </Routes>
    </Router>
  );
}

export default App;