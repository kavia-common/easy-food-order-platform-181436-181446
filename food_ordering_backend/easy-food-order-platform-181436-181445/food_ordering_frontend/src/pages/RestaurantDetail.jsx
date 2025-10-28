import React, { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { apiClient } from '../api/client'
import { useCart } from '../context/CartContext'

function formatPrice(cents) {
  return `$${(cents / 100).toFixed(2)}`
}

export default function RestaurantDetail() {
  const { id } = useParams()
  const client = apiClient()
  const [restaurant, setRestaurant] = useState(null)
  const [menu, setMenu] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const { addItem, items, restaurantId } = useCart()

  useEffect(() => {
    (async () => {
      try {
        const [r, m] = await Promise.all([
          client.get(`/restaurants/${id}`),
          client.get(`/menus/restaurant/${id}`)
        ])
        setRestaurant(r)
        setMenu(m)
      } catch (e) {
        setError('Failed to load restaurant')
      } finally {
        setLoading(false)
      }
    })()
  }, [id])

  if (loading) return <div>Loading...</div>
  if (error) return <div className="error">{error}</div>
  if (!restaurant) return <div>Not found</div>

  return (
    <div>
      <div className="hero">
        <img src={restaurant.image_url || 'https://picsum.photos/seed/food/800/240'} alt={restaurant.name} />
        <div className="hero-text">
          <h2>{restaurant.name}</h2>
          <p>{restaurant.description}</p>
        </div>
      </div>
      <div className="grid">
        {menu.map(mi => (
          <div key={mi.id} className="card">
            <div className="card-body">
              <h3>{mi.name}</h3>
              <p className="muted">{mi.description}</p>
              <div className="row">
                <span className="price">{formatPrice(mi.price_cents)}</span>
                <button className="btn primary" onClick={() => addItem(mi, restaurant.id)}>Add</button>
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="cart-summary">
        <h3>Cart</h3>
        {items.length === 0 ? <p>No items yet.</p> : (
          <>
            <ul>
              {items.map(i => <li key={i.menu_item_id}>{i.name} x {i.quantity} - {formatPrice(i.price_cents * i.quantity)}</li>)}
            </ul>
            <Link to="/checkout" className="btn success">Go to Checkout</Link>
          </>
        )}
        {restaurantId && restaurantId !== Number(id) && <p className="error">Cart contains items from a different restaurant.</p>}
      </div>
    </div>
  )
}
