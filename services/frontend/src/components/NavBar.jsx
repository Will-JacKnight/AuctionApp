import { NavLink } from 'react-router-dom';
import "./../styles/navBar.css"
import { useNavigate, useLocation } from 'react-router-dom';

function NavBar() {

  const navigate  = useNavigate()
  const location = useLocation()

  const logoutOff = location.pathname === "/login" || location.pathname === "/signup"
  const  handleLogout = () => {
    if(sessionStorage.getItem("token")) {
      sessionStorage.removeItem("token")
      alert(" logout Successfull!")
      navigate("/")
    }
  }

    return (
        <nav className="navbar">
        <h1>BiddingHub</h1>
        <ul>
          <li><NavLink to="/" className={({ isActive }) => (isActive ? "active-link" : "")}>Home</NavLink></li>
          <li><NavLink to="/listing" className={({ isActive }) => (isActive ? "active-link" : "")}>Sell</NavLink></li>
          <li><NavLink to="/dashboard" className={({ isActive }) => (isActive ? "active-link" : "")}>Dashboard</NavLink></li>
          {!logoutOff && <img src="/images/logout.png" className='logout-icon' onClick={handleLogout}/>}
          
        </ul>
      </nav>
    )
}

export default NavBar