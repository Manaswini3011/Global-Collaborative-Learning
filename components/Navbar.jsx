import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import '../styles/Navbar.css'

const Navbar = () => {
  const navigate = useNavigate()
  
  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_id')
    navigate('/login')
  }
  
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/dashboard" className="navbar-brand">
          <span className="brand-icon">⚡</span>
          <span className="brand-text">Assessment Orchestrator</span>
        </Link>
        <div className="navbar-links">
          <Link to="/dashboard" className="nav-link">Dashboard</Link>
          <Link to="/intent" className="nav-link">New Intent</Link>
          <button onClick={handleLogout} className="nav-link logout-btn">
            Logout
          </button>
        </div>
      </div>
    </nav>
  )
}

export default Navbar

