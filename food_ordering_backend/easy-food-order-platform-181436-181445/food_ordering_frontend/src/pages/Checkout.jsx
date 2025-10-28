import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useCart } from '../context/CartContext'
import { useAuth } from '../context/AuthContext'
import { apiClient } from '../api/client'

function formatPrice(cents) {
  return `$${(cents / 100).toFixed(2)}`
}

export default function Checkout() {
  const { items, restaurantId, totalCents, clearCart } = useCart()
  const { token } = useAuth()
  const client = apiClient(token)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  async function handlePlaceOrder() {
    setError('')
    setLoading(true)
    try {
      const order = await client.post('/orders', { restaurant_id: restaurantId, items })
      const session = await client.post('/payments/create-checkout-session', { order_id: order.id })
      clearCart()
      // Redirect to payment URL (stubbed -> order success)
      window.location.href = session.checkout_url
    } catch (e) {
      setError('Failed to place order')
    } finally {
      setLoading(false)
    }
  }

  if (!items.length) return <div className="card"><p>Your cart is empty.</p></div>

  return (
    <div className="card">
      <h2>Checkout</h2>
      <ul>
        {items.map(i => <li key={i.menu_item_id}>{i.name} x {i.quantity} - {formatPrice(i.price_cents * i.quantity)}</li>)}
      </ul>
      <h3>Total: {formatPrice(totalCents)}</h3>
      {error && <div className="error">{error}</div>}
      <button className="btn success" onClick={handlePlaceOrder} disabled={loading}>
        {loading ? 'Processing...' : 'Place Order'}
      </button>
    </div>
  )
}
