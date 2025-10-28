from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session
from ..models import Restaurant
from ..schemas import RestaurantOut

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@router.get("", response_model=list[RestaurantOut], summary="List restaurants")
async def list_restaurants(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Restaurant).order_by(Restaurant.id))
    rows = result.scalars().all()
    return rows


@router.get("/{restaurant_id}", response_model=RestaurantOut, summary="Get restaurant by id")
async def get_restaurant(restaurant_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    restaurant = result.scalar_one_or_none()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant
