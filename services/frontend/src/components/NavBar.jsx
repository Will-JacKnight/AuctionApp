import { NavLink } from 'react-router-dom';
import "./../styles/navBar.css"

function NavBar() {
    return (
        <nav className="navbar">
        <h1>BiddingHub</h1>
        <ul>
          <li><NavLink to="/" className={({ isActive }) => (isActive ? "active-link" : "")}>Home</NavLink></li>
          <li><NavLink to="/listing" className={({ isActive }) => (isActive ? "active-link" : "")}>Sell</NavLink></li>
          <li><NavLink to="/dashboard" className={({ isActive }) => (isActive ? "active-link" : "")}>Dashboard</NavLink></li>
        </ul>
      </nav>
    )
}

export default NavBar