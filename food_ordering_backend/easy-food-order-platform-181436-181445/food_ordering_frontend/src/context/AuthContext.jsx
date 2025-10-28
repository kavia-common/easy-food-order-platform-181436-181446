import React, { createContext, useContext, useEffect, useState } from 'react'
import { apiClient } from '../api/client'

const AuthCtx = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem('token') || '')
  const [user, setUser] = useState(null)

  useEffect(() => {
    if (token) localStorage.setItem('token', token)
    else localStorage.removeItem('token')
  }, [token])

  async function login(email, password) {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)
    const res = await fetch((import.meta.env.VITE_API_BASE_URL || 'http://localhost:3001') + '/auth/login', {
      method: 'POST',
      body: formData,
    })
    if (!res.ok) throw new Error('Login failed')
    const data = await res.json()
    setToken(data.access_token)
    setUser({ email })
  }

  async function register(email, password) {
    const client = apiClient()
    await client.post('/auth/register', { email, password })
    return login(email, password)
  }

  function logout() {
    setToken('')
    setUser(null)
  }

  return (
    <AuthCtx.Provider value={{ token, user, login, register, logout }}>
      {children}
    </AuthCtx.Provider>
  )
}

export function useAuth() {
  return useContext(AuthCtx)
}
