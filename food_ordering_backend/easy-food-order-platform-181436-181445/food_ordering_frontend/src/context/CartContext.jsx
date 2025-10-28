import React, { createContext, useContext, useMemo, useState } from 'react'

const CartCtx = createContext(null)

export function CartProvider({ children }) {
  const [restaurantId, setRestaurantId] = useState(null)
  const [items, setItems] = useState([]) // {menu_item_id, quantity, name, price_cents}

  function clearCart() {
    setRestaurantId(null)
    setItems([])
  }

  function addItem(menuItem, restId) {
    if (restaurantId && restId !== restaurantId) {
      // reset cart when switching restaurants
      clearCart()
    }
    if (!restaurantId) setRestaurantId(restId)

    setItems(prev => {
      const idx = prev.findIndex(i => i.menu_item_id === menuItem.id)
      if (idx >= 0) {
        const updated = [...prev]
        updated[idx] = { ...updated[idx], quantity: updated[idx].quantity + 1 }
        return updated
      }
      return [...prev, { menu_item_id: menuItem.id, quantity: 1, name: menuItem.name, price_cents: menuItem.price_cents }]
    })
  }

  function removeItem(menuItemId) {
    setItems(prev => prev.filter(i => i.menu_item_id !== menuItemId))
  }

  function setQty(menuItemId, qty) {
    setItems(prev => prev.map(i => i.menu_item_id === menuItemId ? { ...i, quantity: qty } : i))
  }

  const totalCents = useMemo(() => items.reduce((sum, i) => sum + i.price_cents * i.quantity, 0), [items])

  return (
    <CartCtx.Provider value={{ restaurantId, items, addItem, removeItem, setQty, clearCart, totalCents }}>
      {children}
    </CartCtx.Provider>
  )
}

export function useCart() {
  return useContext(CartCtx)
}
