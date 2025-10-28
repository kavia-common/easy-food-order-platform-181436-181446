import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { apiClient } from '../api/client'

export default function Restaurants() {
  const client = apiClient()
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    (async () => {
      try {
        const res = await client.get('/restaurants')
        setData(res)
      } catch (e) {
        setError('Failed to load restaurants')
      } finally {
        setLoading(false)
      }
    })()
  }, [])

  if (loading) return <div>Loading restaurants...</div>
  if (error) return <div className="error">{error}</div>

  return (
    <div>
      <h2>Restaurants</h2>
      <div className="grid">
        {data.map(r => (
          <Link to={`/restaurants/${r.id}`} key={r.id} className="card restaurant-card">
            <img src={r.image_url || 'https://picsum.photos/seed/food/400/240'} alt={r.name} />
            <div className="card-body">
              <h3>{r.name}</h3>
              <p>{r.description}</p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}
