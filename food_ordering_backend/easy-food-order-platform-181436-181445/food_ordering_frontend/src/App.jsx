import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext.jsx'
import { CartProvider } from './context/CartContext.jsx'
import Login from './pages/Login.jsx'
import Register from './pages/Register.jsx'
import Restaurants from './pages/Restaurants.jsx'
import RestaurantDetail from './pages/RestaurantDetail.jsx'
import Checkout from './pages/Checkout.jsx'
import OrderSuccess from './pages/OrderSuccess.jsx'
import NavBar from './components/NavBar.jsx'

function PrivateRoute({ children }) {
  const { token } = useAuth()
  return token ? children : <Navigate to="/login" />
}

export default function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <div className="app">
          <NavBar />
          <main className="container">
            <Routes>
              <Route path="/" element={<Restaurants />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/restaurants/:id" element={<RestaurantDetail />} />
              <Route path="/checkout" element={<PrivateRoute><Checkout /></PrivateRoute>} />
              <Route path="/order-success" element={<PrivateRoute><OrderSuccess /></PrivateRoute>} />
            </Routes>
          </main>
        </div>
      </CartProvider>
    </AuthProvider>
  )
}
