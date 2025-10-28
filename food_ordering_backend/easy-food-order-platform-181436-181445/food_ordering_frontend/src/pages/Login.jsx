import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const { login } = useAuth()
  const [email, setEmail] = useState('demo@example.com')
  const [password, setPassword] = useState('password')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await login(email, password)
      navigate('/')
    } catch (err) {
      setError('Invalid credentials')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h2>Login</h2>
      <form onSubmit={handleSubmit} className="form">
        <label>Email</label>
        <input value={email} onChange={e => setEmail(e.target.value)} required type="email" />
        <label>Password</label>
        <input value={password} onChange={e => setPassword(e.target.value)} required type="password" />
        {error && <div className="error">{error}</div>}
        <button className="btn primary" disabled={loading} type="submit">{loading ? 'Signing in...' : 'Login'}</button>
      </form>
      <p>New here? <Link to="/register">Create an account</Link></p>
    </div>
  )
}
