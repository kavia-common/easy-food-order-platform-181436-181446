import React from 'react'
import { useSearchParams, Link } from 'react-router-dom'

export default function OrderSuccess() {
  const [params] = useSearchParams()
  const orderId = params.get('order_id')

  return (
    <div className="card">
      <h2>Order Confirmed</h2>
      <p>Your order has been placed successfully{orderId ? ` (ID: ${orderId})` : ''}.</p>
      <Link to="/" className="btn primary">Back to Restaurants</Link>
    </div>
  )
}
