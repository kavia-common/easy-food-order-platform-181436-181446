import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Use DATABASE_URL from env; Expect asyncpg for PostgreSQL. Example:
# DATABASE_URL=postgresql+asyncpg://user:password@host:port/dbname
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./dev.db")

# SQLAlchemy base and engine/session creation
Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# PUBLIC_INTERFACE
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield an AsyncSession for request-scoped DB interactions."""
    async with async_session_factory() as session:
        yield session


# PUBLIC_INTERFACE
async def init_db() -> None:
    """Create database tables if they do not exist."""
    # Import models to register metadata
    from . import models  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# PUBLIC_INTERFACE
async def seed_demo_data() -> None:
    """Seed demo restaurants and menus if database is empty."""
    from sqlalchemy import select
    from .models import Restaurant, MenuItem, User
    from .utils.security import get_password_hash

    async with async_session_factory() as session:
        # If there are restaurants already, assume seeded
        result = await session.execute(select(Restaurant).limit(1))
        if result.scalar_one_or_none():
            return

        # Create a demo user
        demo_user = User(email="demo@example.com", hashed_password=get_password_hash("password"))
        session.add(demo_user)
        await session.flush()

        # Create restaurants
        r1 = Restaurant(name="Pasta Palace", description="Italian favorites", image_url="https://picsum.photos/seed/pasta/400/240")
        r2 = Restaurant(name="Sushi Street", description="Fresh sushi and rolls", image_url="https://picsum.photos/seed/sushi/400/240")
        r3 = Restaurant(name="Burger Barn", description="Burgers, fries, and shakes", image_url="https://picsum.photos/seed/burger/400/240")
        session.add_all([r1, r2, r3])
        await session.flush()

        # Menu items
        items = [
            MenuItem(restaurant_id=r1.id, name="Spaghetti Bolognese", description="Rich meat sauce", price_cents=1299),
            MenuItem(restaurant_id=r1.id, name="Fettuccine Alfredo", description="Creamy alfredo sauce", price_cents=1199),
            MenuItem(restaurant_id=r2.id, name="California Roll", description="Crab, avocado, cucumber", price_cents=899),
            MenuItem(restaurant_id=r2.id, name="Salmon Nigiri", description="Fresh salmon over rice", price_cents=499),
            MenuItem(restaurant_id=r3.id, name="Classic Cheeseburger", description="Cheddar, lettuce, tomato", price_cents=1099),
            MenuItem(restaurant_id=r3.id, name="Loaded Fries", description="Cheese and bacon", price_cents=699),
        ]
        session.add_all(items)

        await session.commit()
