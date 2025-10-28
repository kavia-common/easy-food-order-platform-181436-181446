import os
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db, seed_demo_data
from .routers import auth, restaurants, menus, orders, payments

# Create FastAPI app with metadata and tags for OpenAPI docs
app = FastAPI(
    title="Easy Food Ordering API",
    description="Backend API for authentication, restaurants, menus, orders, and payment stubs.",
    version="0.1.0",
    openapi_tags=[
        {"name": "Auth", "description": "User registration and login"},
        {"name": "Restaurants", "description": "Browse restaurants"},
        {"name": "Menus", "description": "Restaurant menu items"},
        {"name": "Orders", "description": "Create and track orders"},
        {"name": "Payments", "description": "Stripe payment stubs"},
        {"name": "Health", "description": "Health checks and info"},
    ],
)

# CORS configuration: allow requests from frontend at port 3000 by default
frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
allow_origins: List[str] = [frontend_origin]
# Allow any during local dev if wildcard specified
if frontend_origin == "*":
    allow_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"], summary="Health Check")
def health_check():
    """Simple health check endpoint."""
    return {"message": "Healthy"}


# Include routers
app.include_router(auth.router)
app.include_router(restaurants.router)
app.include_router(menus.router)
app.include_router(orders.router)
app.include_router(payments.router)


@app.on_event("startup")
async def on_startup():
    """
    Initialize database and seed demo data on startup.
    This ensures the MVP has some restaurants and menu items available.
    """
    await init_db()
    await seed_demo_data()
