import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Register() {
  const { register } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await register(email, password)
      navigate('/')
    } catch (err) {
      setError('Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h2>Create Account</h2>
      <form onSubmit={handleSubmit} className="form">
        <label>Email</label>
        <input value={email} onChange={e => setEmail(e.target.value)} required type="email" />
        <label>Password</label>
        <input value={password} onChange={e => setPassword(e.target.value)} required type="password" />
        {error && <div className="error">{error}</div>}
        <button className="btn primary" disabled={loading} type="submit">{loading ? 'Creating...' : 'Register'}</button>
      </form>
      <p>Have an account? <Link to="/login">Login</Link></p>
    </div>
  )
}
