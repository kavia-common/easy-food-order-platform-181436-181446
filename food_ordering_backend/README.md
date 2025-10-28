# Easy Food Ordering - Backend (FastAPI)

FastAPI backend providing authentication, restaurants, menus, orders, and stubbed payment endpoints.

## Run

1. Create `.env` from `.env.example` and adjust values.
2. Install deps:
   pip install -r requirements.txt
3. Start:
   uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload

By default uses SQLite file `dev.db`. To use Postgres from the database container, set `DATABASE_URL`:

```
# Example: adapt from your container env
DATABASE_URL=postgresql+asyncpg://$POSTGRES_USER:$POSTGRES_PASSWORD@localhost:$POSTGRES_PORT/$POSTGRES_DB
```

## API

- Health: `GET /`
- Auth:
  - `POST /auth/register` {email, password}
  - `POST /auth/login` form fields: username(email), password -> returns JWT
- Restaurants:
  - `GET /restaurants`
  - `GET /restaurants/{id}`
- Menus:
  - `GET /menus/restaurant/{restaurant_id}`
- Orders:
  - `POST /orders` {restaurant_id, items:[{menu_item_id, quantity}]}
  - `GET /orders`
  - `GET /orders/{order_id}`
- Payments:
  - `POST /payments/create-checkout-session` {order_id} -> returns checkout_url (stub)

Use bearer token in `Authorization: Bearer <token>` header.

## Seed Data

On startup, demo restaurants, menu items, and a demo user (demo@example.com / password) are created if empty.

## CORS

Set `FRONTEND_ORIGIN` (default http://localhost:3000).
