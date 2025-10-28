from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session
from ..models import MenuItem, Restaurant
from ..schemas import MenuItemOut

router = APIRouter(prefix="/menus", tags=["Menus"])


@router.get("/restaurant/{restaurant_id}", response_model=list[MenuItemOut], summary="List menu items for a restaurant")
async def list_menu_items(restaurant_id: int, session: AsyncSession = Depends(get_async_session)):
    # Ensure restaurant exists
    result = await session.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Restaurant not found")

    result2 = await session.execute(select(MenuItem).where(MenuItem.restaurant_id == restaurant_id).order_by(MenuItem.id))
    items = result2.scalars().all()
    return items
