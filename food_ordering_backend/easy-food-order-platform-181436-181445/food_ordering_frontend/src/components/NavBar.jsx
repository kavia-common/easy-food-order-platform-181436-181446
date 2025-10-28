import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useCart } from '../context/CartContext'

export default function NavBar() {
  const { user, token, logout } = useAuth()
  const { items } = useCart()
  const navigate = useNavigate()

  return (
    <header className="navbar">
      <Link to="/" className="brand">EasyFood</Link>
      <nav>
        <Link to="/">Restaurants</Link>
        <Link to="/checkout">Cart ({items.length})</Link>
      </nav>
      <div className="auth">
        {token ? (
          <>
            <span className="muted">{user?.email}</span>
            <button className="btn" onClick={() => { logout(); navigate('/'); }}>Logout</button>
          </>
        ) : (
          <>
            <Link className="btn" to="/login">Login</Link>
            <Link className="btn primary" to="/register">Register</Link>
          </>
        )}
      </div>
    </header>
  )
}
