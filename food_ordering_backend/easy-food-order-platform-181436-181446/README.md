# Easy Food Ordering Platform

This project contains three containers:
- food_ordering_backend (FastAPI) - port 3001
- food_ordering_database (PostgreSQL) - port 5001
- food_ordering_frontend (React) - port 3000

Getting started:
1) Backend
   - cd food_ordering_backend
   - cp .env.example .env and set variables as needed
   - pip install -r requirements.txt
   - uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload

2) Database (optional if using SQLite dev)
   - Use provided env names from work item: POSTGRES_URL, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_PORT
   - Compose a DATABASE_URL for backend: postgresql+asyncpg://$POSTGRES_USER:$POSTGRES_PASSWORD@localhost:$POSTGRES_PORT/$POSTGRES_DB

3) Frontend
   - cd ../food_ordering_frontend
   - cp .env.example .env
   - npm install
   - npm run dev (should run on port 3000)

Open:
- Backend docs: http://localhost:3001/docs
- Frontend: http://localhost:3000

Seed/demo credentials:
- demo@example.com / password

Notes:
- Payments are stubbed; the backend will mark orders as paid when creating a "checkout session" and redirect to /order-success.
- Set FRONTEND_ORIGIN in backend .env if your frontend origin differs.
